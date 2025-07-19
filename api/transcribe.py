from http.server import BaseHTTPRequestHandler
import json
import requests
import os
from dotenv import load_dotenv
import cgi
import subprocess
import math

load_dotenv()

# Chemin vers le binaire ffmpeg (suppose qu'il est à la racine dans un dossier bin)
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), '..', 'bin', 'ffmpeg')

def get_audio_duration(file_content):
    """Obtient la durée d'un fichier audio en utilisant ffprobe."""
    ffprobe_path = FFMPEG_PATH.replace('ffmpeg', 'ffprobe')
    if not os.path.exists(ffprobe_path):
        # ffprobe n'est pas trouvé, on ne peut pas vérifier la durée.
        # On suppose que c'est court pour ne pas bloquer.
        return 0

    command = [
        ffprobe_path,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        '-i', 'pipe:0'
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=file_content)
    
    if process.returncode != 0:
        print(f"Erreur ffprobe: {stderr.decode()}")
        return 0
    
    try:
        return float(stdout)
    except (ValueError, TypeError):
        return 0

def transcribe_chunk(api_key, endpoint, model_id, chunk_data, filename="chunk.wav"):
    """Envoie un segment audio à l'API Mistral."""
    data = {"model": model_id}
    files = {"file": (filename, chunk_data, "audio/wav")}
    headers = {"Authorization": f"Bearer {api_key}"}
    
    r = requests.post(endpoint, headers=headers, data=data, files=files, timeout=120)
    r.raise_for_status()
    return r.json()['text']


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
            MAX_DURATION_SECONDS = 19 * 60  # 19 minutes pour être sûr

            content_type = self.headers.get('Content-Type')
            if not content_type or 'multipart/form-data' not in content_type:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Expected multipart/form-data'}).encode())
                return
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )
            
            if 'file' not in form:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No file in request'}).encode())
                return
            
            file_item = form['file']
            file_content = file_item.file.read()

            duration = get_audio_duration(file_content)
            
            if duration <= MAX_DURATION_SECONDS:
                # Fichier court, transcription directe
                full_transcription = transcribe_chunk(API_KEY, ENDPOINT, MODEL_ID, file_content, file_item.filename)
            else:
                # Fichier long, on segmente avec ffmpeg
                command = [
                    FFMPEG_PATH,
                    '-i', 'pipe:0',          # Entrée depuis stdin
                    '-f', 'segment',         # Format de sortie: segment
                    '-segment_time', str(MAX_DURATION_SECONDS), # Durée de chaque segment
                    '-c', 'copy',            # Copie le codec sans ré-encoder
                    '-map', '0',             # S'assure que toutes les pistes sont mappées
                    '-reset_timestamps', '1',# Réinitialise les timestamps pour chaque segment
                    'pipe:output_%03d.wav'   # Sortie vers un pipe avec un nom de fichier numéroté
                ]
                
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Écriture du contenu du fichier dans l'entrée de ffmpeg
                try:
                    process.stdin.write(file_content)
                    process.stdin.close()
                except (IOError, BrokenPipeError):
                     # Gère le cas où ffmpeg ferme le pipe plus tôt
                    pass

                full_transcription = ""
                # Lecture des segments en sortie de ffmpeg
                # Cette partie est conceptuelle car ffmpeg segment ne peut pas écrire sur stdout directement.
                # On va devoir sauvegarder temporairement les fichiers.
                # Simplifions pour l'instant et supposons que la segmentation fonctionne.
                # Idéalement, il faudrait une approche plus complexe pour gérer les flux de sortie.
                # Pour ce PoC, on va simuler la transcription du premier segment.
                # Note: La segmentation réelle vers stdout est complexe.
                # Cette approche nécessite une révision pour une implémentation de production.
                self.send_response(501)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'La segmentation de fichiers longs n\'est pas encore entièrement implémentée.'}).encode())
                return


            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'text': full_transcription}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e), 'type': type(e).__name__}
            self.wfile.write(json.dumps(error_response).encode())
        
        return 