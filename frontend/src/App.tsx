import { ReactMediaRecorder } from "react-media-recorder";
import { useState, useEffect } from "react";
import "./App.css";
import InstallPWA from "./components/InstallPWA";

function App() {
  const [transcription, setTranscription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  useEffect(() => {
    // Nettoie l'URL de l'objet pour libérer la mémoire lorsque
    // le composant est démonté ou qu'une nouvelle URL est créée.
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const handleStop = (_blobUrl: string, blob: Blob) => {
    setAudioBlob(blob);
    // Crée une nouvelle URL d'objet à partir du blob.
    // C'est plus fiable que d'utiliser celle fournie par la librairie.
    const newAudioUrl = URL.createObjectURL(blob);
    setAudioUrl(newAudioUrl);
    setTranscription("");
    setError(null);
  };

  const handleTranscribe = async () => {
    if (!audioBlob) return;
    
    setIsLoading(true);
    setError(null);
    setTranscription("");

    try {
      const audioFile = new File([audioBlob], "recording.mp3", { type: "audio/mp3" });
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

  const downloadAudio = () => {
    if (!audioBlob) return;
    
    const url = URL.createObjectURL(audioBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `enregistrement-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = () => {
    if (transcription) {
      navigator.clipboard.writeText(transcription).then(() => {
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      }, () => {
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
        render={({ status, startRecording, stopRecording }) => (
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
          </div>
        )}
      />

      {audioUrl && (
        <div className="audio-container">
          <h2>Enregistrement</h2>
          <audio src={audioUrl} controls />
          <div className="audio-actions">
            <button onClick={downloadAudio} className="download-btn">
              Télécharger
            </button>
            <button onClick={handleTranscribe} className="transcribe-btn">
              Transcrire
            </button>
          </div>
        </div>
      )}

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
