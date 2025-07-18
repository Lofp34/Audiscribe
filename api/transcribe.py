from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def transcribe_audio():
    API_KEY = os.getenv("MISTRAL_API_KEY")
    ENDPOINT = "https://api.mistral.ai/v1/audio/transcriptions"
    MODEL_ID = "voxtral-mini-2507"

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_content = file.read()
        
        data = {"model": MODEL_ID}
        files = {"file": (file.filename, file_content, file.content_type)}
        headers = {"Authorization": f"Bearer {API_KEY}"}

        try:
            r = requests.post(
                ENDPOINT,
                headers=headers,
                data=data,
                files=files,
                timeout=120
            )
            r.raise_for_status()
            
            return jsonify(r.json())

        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 