# Updated: backend/app/routers/notes.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.model_utils import load_note_qa_model, process_notes_qa
import tempfile

router = APIRouter()
model = load_note_qa_model()

@router.post("/")
async def analyze_notes(
    file: UploadFile = File(..., description="Clinical notes in .txt or .docx")
):
    try:
        if not file.filename.endswith((".txt", ".docx")):
            raise HTTPException(400, detail="Only .txt or .docx files supported")

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            result = process_notes_qa(tmp.name, model)

        return result

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to process notes", "detail": str(e)}
        )