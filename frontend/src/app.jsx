// frontend/src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import XrayUpload from "./components/XrayUpload";
import VoiceTranscribe from "./components/VoiceTranscribe";
import NoteSummarizer from "./components/NoteSummarizer";
import LabQA from "./components/LabQA";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-8">
        <h1 className="text-3xl font-bold mb-6">MediMateAI: Healthcare Copilot</h1>
        <nav className="mb-6 flex gap-4">
          <Link to="/" className="text-blue-600 hover:underline">X-Ray</Link>
          <Link to="/voice" className="text-blue-600 hover:underline">Transcribe</Link>
          <Link to="/notes" className="text-blue-600 hover:underline">Summarize</Link>
          <Link to="/labqa" className="text-blue-600 hover:underline">Lab Q&A</Link>
        </nav>
        <Routes>
          <Route path="/" element={<XrayUpload />} />
          <Route path="/voice" element={<VoiceTranscribe />} />
          <Route path="/notes" element={<NoteSummarizer />} />
          <Route path="/labqa" element={<LabQA />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
