import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Define the server's host and port
HOST = "0.0.0.0"
PORT = 3000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A custom request handler that requires Bearer Authentication and logs requests.
    """
    
    def _log_request_details(self):
        """Logs authorized requests."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        method = self.command
        user_agent = self.headers.get('User-Agent', 'Not provided')
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "No body"

        print("--- ✅ Authorized Request ---")
        print(f"🕒 Time: {timestamp}")
        print(f"📡 Client IP: {client_ip}")
        print(f"🕵️ User-Agent: {user_agent}")
        print(f"⚙️ Method: {method}")
        print(f"📄 Body: {body}")
        print("--------------------------\n")

    def _send_ok_response(self):
        """Sends a 200 OK response."""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Authorized request received!")

    def _send_unauthorized_response(self):
        """Sends a 401 Unauthorized response for Bearer auth."""
        self.send_response(401)
        # Set the WWW-Authenticate header for Bearer scheme
        self.send_header('WWW-Authenticate', 'Bearer realm="Access denied"')
        self.end_headers()
        self.wfile.write(b'401 Unauthorized: A valid Bearer token is required.')

    def _handle_request(self):
        """Handles an incoming request by checking for a valid Bearer token."""
        required_auth_header = self.server.auth_token
        
        if self.headers.get('Authorization') == required_auth_header:
            self._log_request_details()
            self._send_ok_response()
        else:
            self._send_unauthorized_response()

    # Route all common HTTP methods to the central handler
    def do_GET(self): self._handle_request()
    def do_POST(self): self._handle_request()
    def do_PUT(self): self._handle_request()
    def do_DELETE(self): self._handle_request()
    def do_PATCH(self): self._handle_request()


def run_server():
    """Starts the HTTP server after validating environment variables."""
    auth_token = os.environ.get('AUTH_TOKEN')
    
    if not auth_token:
        print("❌ FATAL: AUTH_TOKEN environment variable not set. Server cannot start.")
        sys.exit(1)

    print("🔑 Bearer token loaded successfully from environment variable.")

    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    # Construct the full "Bearer <token>" header string
    httpd.auth_token = f"Bearer {auth_token}"

    print(f"🚀 Server with Bearer authentication running on http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
