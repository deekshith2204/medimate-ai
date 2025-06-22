# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import labqa, notes, voice, xray

app = FastAPI(
    title="Medical AI API",
    description="Multimodal medical diagnostics: lab, text, voice, and imaging",
    version="1.0.0"
)

# CORS setup (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(labqa.router, prefix="/labqa", tags=["Lab QA"])
app.include_router(notes.router, prefix="/notes", tags=["Clinical Notes"])
app.include_router(voice.router, prefix="/voice", tags=["Voice Transcription"])
app.include_router(xray.router, prefix="/xray", tags=["X-Ray Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Medical AI API"}
