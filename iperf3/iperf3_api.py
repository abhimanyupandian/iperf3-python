import json
import iperf3
import threading

from flask import Flask, request, make_response, jsonify
from ConnectionCache import ConnectionCache

app = Flask(__name__)

_servers = ConnectionCache()
_clients = ConnectionCache()

def _success(data):
    return {
        "data": data
    }

def _error(message):
    return {
    "error": {
        "message": message
        }
    }

@app.route("/server/create", methods=['POST'])
def create_server():
    if request.headers['Content-Type'] == 'application/json':
        name = str(request.json['name'])
    else:
        raise Exception("Server creation Failed : Please provide Client name!")
    server = iperf3.Server()
    server.bind_address = '127.0.0.1'
    server.port = 5201
    server.json_output = False
    _servers.register(server, name)
    return make_response(jsonify(_success(request.data)), 200)

@app.route("/server/<name>/run", methods=['POST', 'PATCH'])
def run_server(name):
    try:
        server = _servers.get_connection(str(name))
        _thread = threading.Thread(target=server.run)
        _thread.daemon = True
        _thread.start()
        return make_response(jsonify(_success(name + " was started")), 200)
    except Exception as e:
        return make_response(jsonify(_error("Server " + name + " start failed : " + str(e))), 501)

@app.route("/server/<string:name>/bind_address", methods=['PATCH'])
def set_server_bind_address(name):
    try:
        server = _servers.get_connection(name)
        if request.headers['Content-Type'] == 'text/plain':
            bind_address = request.data
        elif request.headers['Content-Type'] == 'application/json':
            bind_address = json.dumps(request.json)['bind_address']
        server.bind_address = str(bind_address)
    except Exception as e:
        return make_response(jsonify(_error("Server " + name + " start failed : " + str(e))), 501)
    return server.bind_address

@app.route("/client/create", methods=['POST'])
def create_client():
    if request.headers['Content-Type'] == 'application/json':
        name = str(request.json['name'])
    else:
        raise Exception("Client creation Failed : Please provide Client name!")
    client = iperf3.Client()
    client.duration = 2
    client.server_hostname = '127.0.0.1'
    client.port = 5201
    _clients.register(client, name)
    return make_response(jsonify(_success(request.data)), 200)

@app.route("/client/<name>/run", methods=['POST', 'PATCH'])
def run_client(name):
    try:
        client = _clients.get_connection(str(name))
        results = client.run()
        return make_response(jsonify(_success(str(results.json))), 200)
    except Exception as e:
        return make_response(jsonify(_error("Client " + name + " start failed : " + str(e))), 501)

if __name__ == "__main__":
    app.run(debug=True)
