import json
import sys
import os

def handler(request):
    diagnostics = {
        'python_version': sys.version,
        'python_path': sys.executable,
        'working_directory': os.getcwd(),
        'environment_variables': list(os.environ.keys()),
        'request_method': request.method if hasattr(request, 'method') else 'N/A',
        'request_path': request.path if hasattr(request, 'path') else 'N/A',
        'request_headers': dict(request.headers) if hasattr(request, 'headers') else {},
        'vercel_region': os.environ.get('VERCEL_REGION', 'Not set'),
        'function_name': os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'Not set')
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(diagnostics, indent=2)
    } 