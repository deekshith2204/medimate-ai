# backend/app/routers/xray.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any
from app.utils.model_utils import load_xray_classifier, explain_diagnosis
from PIL import Image
import io

router = APIRouter()
classifier = load_xray_classifier()

@router.post("/", response_model=Dict[str, Any])
async def classify_xray(
    file: UploadFile = File(...),
    generate_notes: bool = Query(False, description="Generate diagnostic notes")
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        predictions = classifier(image)  # ✅ PIL Image only!

        top_pred = predictions[0]
        explanation = explain_diagnosis(top_pred["label"], top_pred["score"]) if generate_notes else ""

        return {
            "label": top_pred["label"],
            "score": top_pred["score"],
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
