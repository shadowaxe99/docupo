import os
from dotenv import load_dotenv
import importlib.util
import json
import openai
import concurrent.futures
import time
from datetime import datetime
from skills.skill import Skill
from skills.skill_registry import SkillRegistry
from tasks.task_registry import TaskRegistry


load_dotenv()  # Load environment variables from .env file

# Retrieve all API keys
api_keys = {
    'openai': os.environ['OPENAI_API_KEY'],
    'serpapi': os.environ['SERPAPI_API_KEY']
    # Add more keys here as needed
}

# Set OBJECTIVE
OBJECTIVE = "Create an example objective and tasklist for 'write a poem', which only uses text_completion in the tasks. Do this by usign code_reader to read example1.json, then writing the JSON objective tasklist pair using text_completion, and saving it using objective_saver."
LOAD_SKILLS = ['text_completion','code_reader','objective_saver']
REFLECTION = False

##### START MAIN LOOP########

# Print OBJECTIVE
print("\033[96m\033[1m"+"\n*****OBJECTIVE*****\n"+"\033[0m\033[0m")
print(OBJECTIVE)

if __name__ == "__main__":
    session_summary = ""
  
    # Initialize the SkillRegistry and TaskRegistry
    skill_registry = SkillRegistry(api_keys=api_keys, skill_names=LOAD_SKILLS)
    skill_descriptions = ",".join(f"[{skill.name}: {skill.description}]" for skill in skill_registry.skills.values())
    task_registry = TaskRegistry()

    # Create the initial task list based on an objective
    task_registry.create_tasklist(OBJECTIVE, skill_descriptions)
  
    # Initialize task outputs
    task_outputs = {i: {"completed": False, "output": None} for i, _ in enumerate(task_registry.get_tasks())}

    # Create a thread pool for parallel execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Loop until all tasks are completed
        while not all(task["completed"] for task in task_outputs.values()):
            
            # Get the tasks that are ready to be executed (i.e., all their dependencies have been completed)
            tasks = task_registry.get_tasks()
            
            # Update task_outputs to include new tasks
            for task in tasks:
                if task["id"] not in task_outputs:
                    task_outputs[task["id"]] = {"completed": False, "output": None}

            ready_tasks = [(task["id"], task) for task in tasks
               if all((dep in task_outputs and task_outputs[dep]["completed"]) 
               for dep in task.get('dependent_task_ids', [])) 
               and not task_outputs[task["id"]]["completed"]]

            session_summary += str(task)+"\n"
            futures = [executor.submit(task_registry.execute_task, task_id, task, skill_registry, task_outputs, OBJECTIVE) 
                       for task_id, task in ready_tasks if not task_outputs[task_id]["completed"]]
            
            # Wait for the tasks to complete
            for future in futures:
                i, output = future.result()
                task_outputs[i]["output"] = output
                task_outputs[i]["completed"] = True
                
                completed_task = task_registry.get_task(i)
                print(f"\033[92mTask #{i}: {completed_task.get('task')} \033[0m\033[92m[COMPLETED]\033[0m\033[92m[{completed_task.get('skill')}]\033[0m")

                # Reflect on the output
                if output:
                    session_summary += str(output)+"\n"

            if all(task["status"] == "completed" for task in task_registry.tasks):
              print("All tasks completed!")
              break
                  
            # Short delay to prevent busy looping
            time.sleep(0.1)


        # Print session summary
        print("\033[96m\033[1m"+"\n*****SAVING FILE...*****\n"+"\033[0m\033[0m")
        file = open(f'output/output_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.txt', 'w')
        file.write(session_summary)
        file.close()
        print("...file saved.")
        print("END")
        executor.shutdown()
import openai
import pinecone
import time
from collections import deque
from typing import Dict, List

# Set API Keys
OPENAI_API_KEY = ""
PINECONE_API_KEY = ""
PINECONE_ENVIRONMENT = "us-east1-gcp" # Pinecone Environment (eg. "us-east1-gcp")

# Set Variables
YOUR_TABLE_NAME = "test-table"
OBJECTIVE = "Solve world hunger."
YOUR_FIRST_TASK = "Develop a task list."

# Print OBJECTIVE
print("\033[96m\033[1m"+"\n*****OBJECTIVE*****\n"+"\033[0m\033[0m")
print(OBJECTIVE)

# Configure OpenAI and Pinecone
openai.api_key = OPENAI_API_KEY
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create Pinecone index
if YOUR_TABLE_NAME not in pinecone.list_indexes():
    pinecone.create_index(YOUR_TABLE_NAME, dimension=1536, metric="cosine", pod_type="p1")

# Connect to the index
index = pinecone.Index(YOUR_TABLE_NAME)

# Task list
task_list = deque([])



def add_task(task: Dict):
    task_list.append(task)



def get_ada_embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]



def task_creation_agent(objective: str, result: Dict, task_description: str, task_list: List[str]):
    prompt = f"You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective}, The last completed task has the result: {result}. This result was based on this task description: {task_description}. These are incomplete tasks: {', '.join(task_list)}. Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Return the tasks as an array."
    response = openai.Completion.create(engine="text-davinci-003",prompt=prompt,temperature=0.5,max_tokens=100,top_p=1,frequency_penalty=0,presence_penalty=0)
    new_tasks = response.choices[0].text.strip().split('\n')
    return [{'task_name': task_name} for task_name in new_tasks]



def prioritization_agent(this_task_id:int):
    global task_list
    task_names = [t['task_name'] for t in task_list]
    next_task_id = int(this_task_id)+1
    prompt = f"""You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing the following tasks: {task_names}. Consider the ultimate objective of your team:{OBJECTIVE}. Do not remove any tasks. Return the result as a numbered list, like:
    #. First task
    #. Second task
    Start the task list with number {next_task_id}."""
    response = openai.Completion.create(engine="text-davinci-003",prompt=prompt,temperature=0.5,max_tokens=1000,top_p=1,frequency_penalty=0,presence_penalty=0)
    new_tasks = response.choices[0].text.strip().split('\n')
    task_list = deque()
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            task_list.append({"task_id": task_id, "task_name": task_name})



def execution_agent(objective:str,task: str) -> str:
    context=context_agent(index=YOUR_TABLE_NAME, query=objective, n=5)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are an AI who performs one task based on the following objective: {objective}. Your task: {task}\nResponse:",
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()



def context_agent(query: str, index: str, n: int):
    query_embedding = get_ada_embedding(query)
    index = pinecone.Index(index)
    results = index.query(query_embedding, top_k=n,
    include_metadata=True)
    sorted_results = sorted(results.matches, key=lambda x: x.score, reverse=True)    
    return [(str(item.metadata['task'])) for item in sorted_results]


# Add the first task
first_task = {
    "task_id": 1,
    "task_name": YOUR_FIRST_TASK
}

add_task(first_task)
# Main loop
task_id_counter = 1
while True:
    if task_list:
        # Print the task list
        print("\033[95m\033[1m"+"\n*****TASK LIST*****\n"+"\033[0m\033[0m")
        for t in task_list:
            print(str(t['task_id'])+": "+t['task_name'])

        # Step 1: Pull the first task
        task = task_list.popleft()
        print("\033[92m\033[1m"+"\n*****NEXT TASK*****\n"+"\033[0m\033[0m")
        print(str(task['task_id'])+": "+task['task_name'])

        # Send to execution function to complete the task based on the context
        result = execution_agent(OBJECTIVE,task["task_name"])
        this_task_id = int(task["task_id"])
        print("\033[93m\033[1m"+"\n*****TASK RESULT*****\n"+"\033[0m\033[0m")
        print(result)

        # Step 2: Enrich result and store in Pinecone
        enriched_result = {'data': result}  # This is where you should enrich the result if needed
        result_id = f"result_{task['task_id']}"
        vector = enriched_result['data']  # extract the actual result from the dictionary
        index.upsert([(result_id, get_ada_embedding(vector),{"task":task['task_name'],'result':result})])

    # Step 3: Create new tasks and reprioritize task list
    new_tasks = task_creation_agent(OBJECTIVE,enriched_result, task["task_name"], [t["task_name"] for t in task_list])

    for new_task in new_tasks:
        task_id_counter += 1
        new_task.update({"task_id": task_id_counter})
        add_task(new_task)
    prioritization_agent(this_task_id)

time.sleep(1)  # Sleep before checking the task list again — include these
