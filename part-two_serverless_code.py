from http.server import BaseHTTPRequestHandler, HTTPServer
import json

memory = {}
printer_mailbox = []

def printer_finished_callback(attendee_name, success=True):
    if success:
        memory[attendee_name] = "Checked-in"
        print(f"Updated {attendee_name} to Checked-in.")
    else:
        memory[attendee_name] = "Failed"
        print(f"Updated {attendee_name} to Failed.")


class handler(BaseHTTPRequestHandler): 
    
    def do_GET(self): 
        """Handle simple browser visits"""
        self.send_response(200)
        # Removed the duplicate content-type line to keep it clean
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response_data = {"message": "Hello! Welcome to serverless paradise!"}            
        self.wfile.write(json.dumps(response_data).encode())

    def do_POST(self):
        """Handle webhook callbacks from the printer"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        attendee_name = data.get('name')
        success = data.get('success', True)
        
        if attendee_name:
            printer_finished_callback(attendee_name, success)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response_data = {"status": "Webhook received"}
        self.wfile.write(json.dumps(response_data).encode())

if __name__ == "__main__":
    print("Starting server on port 8000...")
    server = HTTPServer(('localhost', 8000), handler)
    print("Server is running! Check the terminal for messages.")
    server.serve_forever()
