import http.server
import socketserver
import json
import os
from threading import Lock

PORT = 58541
data_lock = Lock()

def load_data(default_data):
    with data_lock:  # Ensure thread-safe file access
        if not os.path.isfile('data.json'):
            with open('data.json', 'w') as f:
                json.dump(default_data, f)
            return default_data
        else:
            try:
                with open('data.json', 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Handle the case where the JSON file is corrupt or empty
                with open('data.json', 'w') as f:
                    json.dump(default_data, f)
                return default_data

# Define the default data structure at the top of your script
default_data_structure = {
    'total_loads': 0,
    'unique_visitors': []
}

def save_data(data):
    with data_lock:  # Ensure thread-safe file access
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
        self.server_version = "MyHTTP/"  # Customize the server name if desired
        self.sys_version = ""  # Hide the Python version
        # Update data with the IP of the client making the request
        update_data(self.client_address[0])
        # Call superclass method to actually handle the request
        super().do_GET()

    def log_message(self, format, *args):
        # We override this method to prevent printing to the console
        pass

Handler = LoggingHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
