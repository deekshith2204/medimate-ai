// frontend/src/components/VoiceTranscribe.jsx
import React, { useState } from "react";
import axios from "axios";

const VoiceTranscribe = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTranscribe = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/voice", formData);
      setText(res.data.transcription);
    } catch (e) {
      console.error("Transcription failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Transcribe Voice Note</h2>
      <input
        type="file"
        accept="audio/wav"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleTranscribe}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
      >
        Transcribe
      </button>
      {loading && <p className="mt-4">Transcribing...</p>}
      {text && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Transcript:</h3>
          <p className="text-gray-800 bg-gray-100 p-2 rounded">{text}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceTranscribe;
