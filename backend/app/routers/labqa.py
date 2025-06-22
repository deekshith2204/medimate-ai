# backend/app/routers/labqa.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.utils.model_utils import load_tapas_model, process_labqa
import pandas as pd
import tempfile
from typing import Dict, Any

router = APIRouter()

# Load model once at startup
model = load_tapas_model()

@router.post("/", response_model=Dict[str, Any])
async def answer_lab_question(
    file: UploadFile = File(..., description="CSV file with lab results"),
    question: str = Form(..., example="What was Patient X's HbA1c on July 15?")
):
    """Analyze structured lab reports with NLP"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(400, detail="Only CSV files accepted")

        # Secure temp file handling
        content = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(content)
            tmp.flush()
            tmp_path = tmp.name

        try:
            df = pd.read_csv(tmp_path)
        except pd.errors.EmptyDataError:
            raise HTTPException(400, detail="Empty CSV file")

        # Process using shared model utility
        result = process_labqa(df, question, model)

        return {
            "answer": result["answer"],
            "confidence": float(result["confidence"]),
            "cells_used": result["cells"]
        }

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Processing failed", "detail": str(e)}
        )
    finally:
        if 'tmp_path' in locals():
            try:
                os.remove(tmp_path)
            except Exception:
                pass
