from http.server import BaseHTTPRequestHandler, HTTPServer
import json

memory = {}

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = {"status": "Webhook server running"}
        self.wfile.write(json.dumps(message).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        name = data.get('name')
        success = data.get('success', True)
        
        if success:
            memory[name] = "Checked-in"
            print("Checked in:", name)
        else:
            memory[name] = "Failed"
            print("Failed:", name)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = {"status": "Webhook received"}
        self.wfile.write(json.dumps(message).encode())

if __name__ == "__main__":
    print("Webhook server starting on port 8001")
    server = HTTPServer(('localhost', 8001), handler)
    server.serve_forever()