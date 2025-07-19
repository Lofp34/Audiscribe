import { ReactMediaRecorder } from "react-media-recorder";
import { useState } from "react";
import "./App.css";
import InstallPWA from "./components/InstallPWA";

function App() {
  const [transcription, setTranscription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState(false);

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

  const copyToClipboard = () => {
    if (transcription) {
      navigator.clipboard.writeText(transcription).then(() => {
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000); // Réinitialise après 2 secondes
      }, () => {
        // Gérer l'échec de la copie si nécessaire
        console.error("Échec de la copie dans le presse-papiers");
      });
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
        <div className="transcription-header">
          <h2>Transcription</h2>
          {transcription && (
            <button onClick={copyToClipboard} className="copy-btn">
              {copySuccess ? "Copié !" : "Copier"}
            </button>
          )}
        </div>
        {isLoading && <p className="loading">Transcription en cours...</p>}
        {error && <p className="error">Erreur: {error}</p>}
        {transcription && <p className="transcription-text">{transcription}</p>}
      </div>
      
      <InstallPWA />
    </div>
  );
}

export default App;
