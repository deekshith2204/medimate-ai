// frontend/src/components/LabQA.jsx
import React, { useState } from "react";
import axios from "axios";

const LabQA = () => {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQA = async () => {
    if (!file || !question.trim()) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);
    try {
      const res = await axios.post("http://localhost:8000/labqa", formData);
      setAnswer(res.data.answer);
    } catch (e) {
      console.error("QA failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg max-w-xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Lab Report Q&A</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <input
        type="text"
        placeholder="Ask a question about the lab results..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full p-2 border rounded mb-4"
      />
      <button
        onClick={handleQA}
        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
      >
        Ask
      </button>
      {loading && <p className="mt-4">Processing...</p>}
      {answer && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Answer:</h3>
          <p className="text-gray-800 bg-gray-100 p-2 rounded whitespace-pre-wrap">{answer}</p>
        </div>
      )}
    </div>
  );
};

export default LabQA;
