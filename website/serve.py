import http.server
import socketserver

PORT = 58541

class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        with open("log.txt", "a") as file:
            file.write("%s - - [%s] %s\n" %
                       (self.client_address[0],
                        self.log_date_time_string(),
                        format%args))

Handler = LoggingHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
