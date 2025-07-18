import argparse, os, sys, requests, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")
assert API_KEY, "Ajoute MISTRAL_API_KEY dans .env"

ENDPOINT = "https://api.mistral.ai/v1/audio/transcriptions"
MODEL_ID = "voxtral-mini-2507"

def transcribe(file: Path, lang=None):
    if not file.exists():
        sys.exit(f"❌ Fichier introuvable: {file}")
    data  = {"model": MODEL_ID}
    if lang:
        data["language"] = lang
    with file.open("rb") as f:
        r = requests.post(
            ENDPOINT,
            headers={"x-api-key": API_KEY},
            data=data,
            files={"file": (file.name, f, "application/octet-stream")},
            timeout=120
        )
    print("HTTP", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except ValueError:
        print(r.text)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--lang")
    transcribe(Path(p.parse_args().file), p.parse_args().lang)
