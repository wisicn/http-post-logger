import os
import sys
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# --- Configure logging ---
# Set the format to '%(message)s' to output the log string exactly as we create it,
# without any extra timestamps or log levels from the logger itself.
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Define the server's host and port
HOST = "0.0.0.0"
PORT = 3000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Handler using the logging module with a custom multi-line format."""

    # This silences the default "172.17.0.1 - - ..." log lines
    def log_message(self, format, *args):
        return

    def _log_request_details(self):
        """Builds a multi-line string and passes it to the logger."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        method = self.command
        user_agent = self.headers.get('User-Agent', 'Not provided')
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "No body"

        # 1. Construct the entire multi-line message as a single f-string
        log_output = (
            f"--- ✅ Authorized Request ---\n"
            f"🕒 Time: {timestamp}\n"
            f"📡 Client IP: {client_ip}\n"
            f"🕵️ User-Agent: {user_agent}\n"
            f"⚙️ Method: {method}\n"
            f"📄 Body: {body}\n"
            f"--------------------------\n"
        )
        
        # 2. Pass the complete, formatted string to the logger
        logging.info(log_output)
    
    # ... (the rest of your handler methods remain the same) ...

    def _send_ok_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Authorized request received!")

    def _send_unauthorized_response(self):
        # We can also create a custom format for unauthorized requests
        logging.warning(
            f"--- ❌ Unauthorized Request from {self.client_address[0]} ---\n"
        )
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Bearer realm="Access denied"')
        self.end_headers()
        self.wfile.write(b'401 Unauthorized: A valid Bearer token is required.')

    def _handle_request(self):
        required_auth_header = self.server.auth_token
        if self.headers.get('Authorization') == required_auth_header:
            self._log_request_details()
            self._send_ok_response()
        else:
            self._send_unauthorized_response()

    def do_GET(self): self._handle_request()
    def do_POST(self): self._handle_request()
    def do_PUT(self): self._handle_request()
    def do_DELETE(self): self._handle_request()
    def do_PATCH(self): self._handle_request()

def run_server():
    """Starts the HTTP server."""
    auth_token = os.environ.get('AUTH_TOKEN')
    
    if not auth_token:
        # Using logging.critical for fatal errors
        logging.critical("FATAL: AUTH_TOKEN environment variable not set. Server cannot start.")
        sys.exit(1)

    logging.info("🔑 Bearer token loaded successfully from environment variable.")
    logging.info(f"🚀 Server with Bearer authentication running on http://{HOST}:{PORT}\n")
    
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.auth_token = f"Bearer {auth_token}"
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nShutting down the server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
