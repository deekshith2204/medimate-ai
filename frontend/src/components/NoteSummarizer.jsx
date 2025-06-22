// frontend/src/components/NoteSummarizer.jsx
import React, { useState } from "react";
import axios from "axios";

const NoteSummarizer = () => {
  const [inputText, setInputText] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/notes", { text: inputText });
      setSummary(res.data.summary);
    } catch (e) {
      console.error("Summarization failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg max-w-xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Summarize Doctor Notes</h2>
      <textarea
        className="w-full h-32 p-2 border rounded mb-4"
        placeholder="Paste clinical notes here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button
        onClick={handleSummarize}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Summarize
      </button>
      {loading && <p className="mt-4">Summarizing...</p>}
      {summary && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Summary:</h3>
          <p className="text-gray-800 bg-gray-100 p-2 rounded whitespace-pre-wrap">{summary}</p>
        </div>
      )}
    </div>
  );
};

export default NoteSummarizer;
