from AIAssistant import AIAssistant

# Initialize the AI assistant
assistant = AIAssistant()

# Get user input
user_input = input('Enter your query: ')

# Process user input
try:
    response = assistant.interact(user_input)
except Exception as e:
    response = f'An error occurred: {e}'

# Print the response
print(response)
