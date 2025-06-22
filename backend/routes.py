# backend/routes.py (updated to use shared model loader)

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import pandas as pd
import tempfile

from model_loader import (
    get_xray_pipeline,
    get_summarizer,
    get_asr_pipeline,
    get_csv_qa_pipeline
)

router = APIRouter()

@router.post("/xray")
async def diagnose_xray(file: UploadFile = File(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(contents)
        temp.flush()
        img = Image.open(temp.name)
    results = get_xray_pipeline()(img)
    return JSONResponse(content=results)

@router.post("/summarize")
async def summarize_notes(text: str = Form(...)):
    summary = get_summarizer()(text, max_length=80, min_length=20, do_sample=False)
    return {"summary": summary[0]['summary_text']}

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(contents)
        temp.flush()
        transcript = get_asr_pipeline()(temp.name)
    return {"text": transcript['text']}

@router.post("/labqa")
async def lab_report_qa(file: UploadFile = File(...), question: str = Form(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp:
        temp.write(contents)
        temp.flush()
        df = pd.read_csv(temp.name)
    answer = get_csv_qa_pipeline()(table=df, query=question)
    return {"answer": answer['answer']}

@router.get("/ping")
def health_check():
    return {"status": "ok"}
