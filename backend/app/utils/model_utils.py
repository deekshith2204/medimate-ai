# backend/app/utils/model_utils.py
import torch
from transformers import pipeline,AutoTokenizer, AutoModelForQuestionAnswering
from PIL import Image
import numpy as np
import io
import re
import pandas as pd
import docx
import os

DEVICE = 0 if torch.cuda.is_available() else -1

# ------------------- LABQA -------------------
def load_tapas_model():
    return pipeline("table-question-answering", model="google/tapas-large-finetuned-wtq", device=DEVICE)

def process_labqa(df, question, pipe):
    df = df.astype(str)
    result = pipe(table=df, query=question)
    return {
        "answer": result["answer"],
        "confidence": result.get("score", 1.0),
        "cells": result.get("coordinates", [])
    }

# ------------------- VOICE -------------------
def load_asr_pipeline():
    return pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-large-v3",
        device=DEVICE,
        torch_dtype=torch.float16 if DEVICE == 0 else torch.float32
    )

def extract_medical_terms(text: str) -> list[str]:
    patterns = [
        r"\b[A-Z][a-z]+['-]?[A-Z][a-z]+\b",
        r"\b\d+[\/-]\d+\b",
        r"\b[A-Z]{2,}\b"
    ]
    terms = set()
    for pattern in patterns:
        terms.update(re.findall(pattern, text))
    return sorted(terms)

# ------------------- XRAY -------------------
def load_xray_classifier():
    return pipeline(
        "image-classification",
        model="shashankrai/chexnet_vanilla",
        device=DEVICE
    )

def preprocess_xray(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    image = image.resize((224, 224))
    arr = np.array(image) / 255.0
    return torch.tensor(arr).permute(2, 0, 1).unsqueeze(0).float()

def detect_exposure(image: Image.Image) -> bool:
    arr = np.array(image.convert("L"))
    return (arr > 240).mean() > 0.3

def explain_diagnosis(label: str, score: float) -> str:
    explanations = {
        "Atelectasis": "Partial lung collapse",
        "Cardiomegaly": "Enlarged heart size",
        "Consolidation": "Lung filled with liquid",
        "Edema": "Fluid in lungs",
        "Pleural Effusion": "Fluid between lung and chest"
    }
    return f"{explanations.get(label, label)} ({score:.1%} confidence)"

#----------- nots-------------
def load_note_qa_model():
    """
    Load a pre-trained question-answering model from Hugging Face.
    You can replace this with a model fine-tuned for clinical notes if needed.
    """
    model_name = "distilbert-base-cased-distilled-squad"  # Replace with clinical-specific model if available
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    return qa_pipeline

def read_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            import docx
            doc = docx.Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            raise ValueError("Unsupported file format.")


def process_notes_qa(filepath, model):
    """
    Process clinical notes using a QA model. As an example, we'll ask generic medical questions.
    """
    context = read_file_content(filepath)

    # Sample questions for demo purposes
    sample_questions = [
        "What symptoms are mentioned?",
        "What medications are prescribed?",
        "What is the diagnosis?",
        "Is there any follow-up recommendation?",
    ]

    answers = []
    for question in sample_questions:
        try:
            result = model(question=question, context=context)
            answers.append({
                "question": question,
                "answer": result["answer"],
                "score": result["score"]
            })
        except Exception as e:
            answers.append({
                "question": question,
                "error": str(e)
            })

    return {"results": answers}