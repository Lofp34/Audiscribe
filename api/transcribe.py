from http.server import BaseHTTPRequestHandler
import requests
import os
from dotenv import load_dotenv
import cgi

load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        API_KEY = os.getenv("MISTRAL_API_KEY")
        ENDPOINT = "https://api.mistral.ai/v1/audio/transcriptions"
        MODEL_ID = "voxtral-mini-2507"

        # Parse the form data to get the file
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        
        if 'file' in form:
            file_item = form['file']
            if file_item.filename:
                # The file is received as a binary stream
                file_content = file_item.file.read()
                
                # Prepare the request for Mistral AI API
                data = {"model": MODEL_ID}
                files = {"file": (file_item.filename, file_content, "application/octet-stream")}
                headers = {"Authorization": f"Bearer {API_KEY}"}

                try:
                    r = requests.post(
                        ENDPOINT,
                        headers=headers,
                        data=data,
                        files=files,
                        timeout=120
                    )
                    r.raise_for_status()  # Raise an exception for bad status codes
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(r.text.encode('utf-8'))

                except requests.exceptions.RequestException as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(str(e).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"No file uploaded.")
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"File not found in form data.")
        return 