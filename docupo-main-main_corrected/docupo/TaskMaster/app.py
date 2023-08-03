from flask import Flask
from user import User
from task import Task
from feedback import Feedback
from ai_agent import AIAgent

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()