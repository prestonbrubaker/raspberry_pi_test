import socket
import http.server
import socketserver
import json
import os
from threading import Lock

PORT = 58541
data_lock = Lock()

def load_data(default_data):
    with data_lock:
        if not os.path.isfile('data.json'):
            with open('data.json', 'w') as f:
                json.dump(default_data, f)
            return default_data
        else:
            try:
                with open('data.json', 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error reading the JSON file: JSONDecodeError")
                with open('data.json', 'w') as f:
                    json.dump(default_data, f)
                return default_data

default_data_structure = {
    'total_loads': 0,
    'unique_visitors': []
}

def save_data(data):
    with data_lock:
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

def update_data(ip):
    data = load_data(default_data_structure)
    data['total_loads'] += 1
    if ip not in data['unique_visitors']:
        data['unique_visitors'].append(ip)
    save_data(data)

class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        update_data(self.client_address[0])
        super().do_GET()

    def log_message(self, format, *args):
        pass

Handler = LoggingHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
