import { ReactMediaRecorder } from "react-media-recorder";
import { useState } from "react";
import "./App.css";

function App() {
  const [transcription, setTranscription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStop = async (_blobUrl: string, blob: Blob) => {
    setIsLoading(true);
    setError(null);
    setTranscription("");

    try {
      const audioFile = new File([blob], "recording.mp3", { type: "audio/mp3" });
      const formData = new FormData();
      formData.append("file", audioFile);

      const response = await fetch("/api/transcribe", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur du serveur: ${response.statusText}`);
      }

      const data = await response.json();
      setTranscription(data.text);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Une erreur inconnue est survenue.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Audio Scribe</h1>
      <p>Enregistrez votre voix et obtenez la transcription instantanément.</p>
      
      <ReactMediaRecorder
        audio
        onStop={handleStop}
        render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
          <div className="recorder">
            <div className="controls">
              <button onClick={startRecording} disabled={status === "recording"}>
                Démarrer
              </button>
              <button onClick={stopRecording} disabled={status !== "recording"}>
                Arrêter
              </button>
            </div>
            <p className="status">Statut: <span>{status}</span></p>
            {mediaBlobUrl && status === 'stopped' && <audio src={mediaBlobUrl} controls />}
          </div>
        )}
      />

      <div className="transcription-container">
        <h2>Transcription</h2>
        {isLoading && <p className="loading">Transcription en cours...</p>}
        {error && <p className="error">Erreur: {error}</p>}
        {transcription && <p className="transcription-text">{transcription}</p>}
      </div>
    </div>
  );
}

export default App;
