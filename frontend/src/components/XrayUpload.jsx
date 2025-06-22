// frontend/src/components/XrayUpload.jsx
import React, { useState } from "react";
import axios from "axios";

const XrayUpload = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/xray", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data.predictions);
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg max-w-md mx-auto">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload X-ray
      </button>
      {loading && <p className="mt-4">Analyzing...</p>}
      {result && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Prediction:</h3>
          <ul>
            {result.map((item, idx) => (
              <li key={idx}>
                {item.label}: <strong>{(item.score * 100).toFixed(2)}%</strong>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default XrayUpload;
