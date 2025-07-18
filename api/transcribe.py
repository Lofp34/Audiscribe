import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def handler(request):
    # Check if this is a POST request
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    API_KEY = os.getenv("MISTRAL_API_KEY")
    ENDPOINT = "https://api.mistral.ai/v1/audio/transcriptions"
    MODEL_ID = "voxtral-mini-2507"
    
    try:
        # Parse the multipart form data
        # In Vercel's Python runtime, the body might be base64 encoded
        import base64
        import cgi
        from io import BytesIO
        
        # Get the body content
        body = request.body
        if isinstance(body, str):
            body = body.encode('utf-8')
        
        # Parse multipart form data
        headers = request.headers
        content_type = headers.get('content-type', '')
        
        if 'multipart/form-data' not in content_type:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Expected multipart/form-data'})
            }
        
        # Create a BytesIO object from the body
        body_file = BytesIO(body)
        
        # Parse the form
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(body))
        }
        
        form = cgi.FieldStorage(
            fp=body_file,
            environ=environ,
            keep_blank_values=True
        )
        
        if 'file' not in form:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No file in request'})
            }
        
        file_item = form['file']
        if not file_item.filename:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No filename'})
            }
        
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(r.json())
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'type': type(e).__name__})
        } 