#  Medimate-AI: Multimodal Medical Diagnostics API

**Medimate-AI** is a smart healthcare assistant powered by AI. It provides **multimodal diagnostic support** using clinical text, lab reports, voice transcriptions, and X-ray images.

This project is built using **FastAPI**, Hugging Face Transformers, and state-of-the-art deep learning models. It demonstrates my ability to integrate multiple AI modalities into a unified API system – an essential skill for data science, ML engineering, and AI-driven product roles.

---

##  Key Features

| Modality     | Capability                                      |
|--------------|-------------------------------------------------|
|  X-Ray       | Image classification + clinical note generation |
|  Clinical Notes | QA over `.txt` or `.docx` formatted text     |
|  Lab Reports | Table QA using TAPAS model                      |
|  Voice       | Transcription and medical term highlighting     |

---

##  Project Objectives

-  **Demonstrate real-world healthcare AI use cases**
-  Combine **NLP**, **CV**, **Speech**, and **structured data** analysis
-  Build and expose **REST APIs** with clean documentation (Swagger/OpenAPI)
-  Optimize inference with GPU/CPU switching and memory handling

---

##  Use Cases

-  Doctors can query lab reports using natural language.
-  Nurses or physicians can upload clinical notes and extract insights.
-  Transcribe doctor-patient conversations and highlight key terms.
-  Diagnose chest X-rays with optional auto-generated notes.

---

##  Tech Stack

| Area         | Tool / Library                           |
|--------------|------------------------------------------|
| Backend      | FastAPI, Uvicorn, Pydantic               |
| ML/NLP       | transformers, torch, scikit-learn        |
| CV/X-ray     | Pillow, ResNet, CheXNet                  |
| Speech       | Whisper (openai/whisper-large-v3)        |
| QA Models    | APAS, DistilBERT                         |
| File I/O     | pandas, python-docx, multipart           |

---

##  API Overview

You can interact with the following endpoints:

| Endpoint      | Method | Description                          |
|---------------|--------|--------------------------------------|
| `/labqa/`     | POST   | Ask questions about lab CSV files    |
| `/notes/`     | POST   | Analyze and extract QA from notes    |
| `/voice/`     | POST   | Transcribe `.mp3/.wav` and extract medical terms |
| `/xray/`      | POST   | Classify and optionally explain X-ray images |

Auto docs available at: `http://localhost:8000/docs`

---


