from flask import Flask, jsonify

app = Flask(__name__)

class NotificationSystem:

    def __init__(self):
        self.messages = {
            'UPLOAD_SUCCESS': 'Document uploaded successfully.',
            'UPLOAD_FAILURE': 'Document upload failed.',
            'REPO_SUCCESS': 'Repository created successfully.',
            'REPO_FAILURE': 'Repository creation failed.'
        }

    def notifyUser(self, message_key):
        message = self.messages.get(message_key)
        if message:
            return jsonify({'message': message})
        else:
            return jsonify({'message': 'Unknown status.'})

@app.route('/notify/<string:message_key>', methods=['GET'])
def notify(message_key):
    notification_system = NotificationSystem()
    return notification_system.notifyUser(message_key)

if __name__ == '__main__':
    app.run(debug=True)
```