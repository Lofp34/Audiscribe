from http.server import BaseHTTPRequestHandler
import json
import requests
import os
from dotenv import load_dotenv
import cgi

load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            API_KEY = os.getenv("MISTRAL_API_KEY")
            if not API_KEY:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'MISTRAL_API_KEY not found'}).encode())
                return
            
            ENDPOINT = "https://api.mistral.ai/v1/audio/transcriptions"
            MODEL_ID = "voxtral-mini-2507"
            
            # Parse the multipart form data
            content_type = self.headers.get('Content-Type')
            if not content_type or 'multipart/form-data' not in content_type:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Expected multipart/form-data'}).encode())
                return
            
            # Parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
            
            if 'file' not in form:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No file in request'}).encode())
                return
            
            file_item = form['file']
            if not file_item.filename:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No filename'}).encode())
                return
            
            # Get file content
            file_content = file_item.file.read()
            
            # Prepare request to Mistral
            data = {"model": MODEL_ID}
            files = {"file": (file_item.filename, file_content, "application/octet-stream")}
            headers = {"Authorization": f"Bearer {API_KEY}"}
            
            # Make request to Mistral
            r = requests.post(
                ENDPOINT,
                headers=headers,
                data=data,
                files=files,
                timeout=120
            )
            
            r.raise_for_status()
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(r.text.encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.wfile.write(json.dumps(error_response).encode())
        
        return 