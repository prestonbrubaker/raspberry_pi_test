import http.server
import socketserver
import json
import os

PORT = 58541



def load_data(default_data):
    if not os.path.isfile('data.json'):
        with open('data.json', 'w') as f:
            json.dump(default_data, f)
        return default_data
    else:
        try:
            with open('data.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Handle the case where the JSON is not able to be decoded
            print("Error reading the JSON file: JSONDecodeError")
            return default_data

# Usage
default_data_structure = {
    'total_loads': 0,
    'unique_visitors': set()
}
data = load_data(default_data_structure)


# Save the current counts to a file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Update the counts and save to the file
def update_data(ip):
    data = load_data()
    data['total_loads'] += 1
    data['unique_ips'].add(ip)
    save_data(data)

class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Update data with the IP of the client making the request
        update_data(self.client_address[0])
        
        # Call superclass method to actually handle the request
        super().do_GET()

    def log_message(self, format, *args):
        # We override this method to prevent printing to the console
        pass

Handler = LoggingHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
