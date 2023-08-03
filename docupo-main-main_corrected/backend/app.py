from flask import Flask, request, jsonify
from document_parser import parseDocument
from repository_generator import generateRepoStructure
from github_integration import createGithubRepo, pushToGithub
from notification_system import notifyUser

app = Flask(__name__)

DOCUMENT_FORMATS = ['pdf', 'docx', 'txt']
GITHUB_API_KEY = 'your_github_api_key'

@app.route('/upload', methods=['POST'])
def uploadDocument():
    file = request.files['document']
    if file and file.filename.rsplit('.', 1)[1].lower() in DOCUMENT_FORMATS:
        document_data = parseDocument(file)
        repo_structure = generateRepoStructure(document_data)
        return jsonify(repo_structure), 200
    else:
        return jsonify({'message': 'Invalid file format'}), 400

@app.route('/review', methods=['POST'])
def reviewRepoStructure():
    repo_structure = request.json.get('repo_structure')
    if repo_structure:
        repo_url = createGithubRepo(GITHUB_API_KEY, repo_structure)
        pushToGithub(GITHUB_API_KEY, repo_url, repo_structure)
        notifyUser('REPO_SUCCESS')
        return jsonify({'message': 'Repository created successfully'}), 200
    else:
        return jsonify({'message': 'Invalid repository structure'}), 400

if __name__ == '__main__':
    app.run(debug=True)
```