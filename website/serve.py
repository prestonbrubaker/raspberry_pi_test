import http.server
import socketserver
import json

PORT = 58541

# Load the existing data if available
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"total_loads": 0, "unique_ips": set()}

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
