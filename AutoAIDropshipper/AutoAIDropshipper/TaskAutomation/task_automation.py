import openai
from chromadb import ChromaClient

openai.api_key = '<openai_api_key>'

client = ChromaClient('http://localhost:8000')

def get_task():
  task = client.query_vector('SELECT * FROM tasks WHERE status = "todo" LIMIT 1')
  return task

def mark_task_done(task):
  task['status'] = 'done'
  client.insert_vector(task)

def generate_response(task):
  response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=f"Complete this task: {task["description"]}",
    max_tokens=1024
  ).choices[0].text
  
  return response

def main():

  while True:
    task = get_task()
    
    if not task:
      break
      
    response = generate_response(task)
    
    mark_task_done(task)
    
main()