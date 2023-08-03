from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/retrieve_node/<node_id>', methods=['GET'])
def retrieve_node(node_id):
    # Retrieve a node from the knowledge graph
    # ...
    # Return the node data
    return jsonify({'node': node_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
