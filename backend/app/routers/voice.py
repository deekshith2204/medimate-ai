# backend/app/routers/voice.py
from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse
from app.utils.model_utils import load_asr_pipeline, extract_medical_terms
import tempfile

router = APIRouter()

pipe = load_asr_pipeline()

@router.post("/")
async def transcribe_audio(
    file: UploadFile = File(...),
    highlight_medical: bool = Query(default=True)
):
    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(contents)
            tmp.flush()
            audio_path = tmp.name

        # Whisper pipeline call (DO NOT pass language here!)
        result = pipe(audio_path)

        text = result.get("text", "")
        response = {
            "transcription": text,
            "confidence": result.get("score", None),
            "language": result.get("language", "unknown")  # Optional
        }

        if highlight_medical:
            response["medical_terms"] = extract_medical_terms(text)

        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "detail": str(e)
        })
