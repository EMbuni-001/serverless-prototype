from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

memory = {}

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = {"Status": "Server is running"}
        self.wfile.write(json.dumps(message).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        name = data.get('name')
        
        if name in memory:
            status = memory[name]
            if status == "Pending":
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                message = {"Error": "Waiting for badge"}
                self.wfile.write(json.dumps(message).encode())
                return
            elif status == "Checked-in":
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                message = {"Error": "Already checked in"}
                self.wfile.write(json.dumps(message).encode())
                return
        
        memory[name] = "Pending"
        print("Badge printing for:", name)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = {"Status": "Pending", "Message": "Printing badge"}
        self.wfile.write(json.dumps(message).encode())

if __name__ == "__main__":
    print("Server starting on port 8000")
    server = HTTPServer(('localhost', 8000), handler)
    server.serve_forever()

    
