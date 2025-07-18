from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        diagnostics = {
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'environment_variables': list(os.environ.keys()),
            'vercel_region': os.environ.get('VERCEL_REGION', 'Not set'),
            'api_directory_contents': os.listdir('api') if os.path.exists('api') else 'api directory not found',
            'request_path': self.path,
            'request_headers': dict(self.headers)
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(diagnostics, indent=2).encode())
        return 