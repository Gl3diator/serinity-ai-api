from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_ID = os.getenv("MODEL_ID", "AnasAlokla/multilingual_go_emotions_V1.2")
DEFAULT_THRESHOLD = float(os.getenv("DEFAULT_THRESHOLD", "0.5"))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "256"))
MAX_LABEL_COUNT = 28

app = FastAPI(title="Serinity AI API", version="0.1.0")


class PredictRequest(BaseModel):
    text: str = Field(min_length=1, description="Journal text content")
    threshold: float | None = Field(default=None, ge=0.0, le=1.0)
    top_k: int | None = Field(default=None, ge=1, le=MAX_LABEL_COUNT)
    include_all_scores: bool = False

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("text must not be blank")
        return value.strip()


class LabelScore(BaseModel):
    label: str
    score: float


class PredictResponse(BaseModel):
    model: str
    problem_type: str
    text: str
    threshold_used: float
    top_k_used: int
    labels: list[LabelScore]
    top_label: str
    all_scores: list[LabelScore] | None


@lru_cache(maxsize=1)
def get_model_resources() -> tuple[Any, Any]:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    model.eval()
    return tokenizer, model


@app.on_event("startup")
def load_model_on_startup() -> None:
    get_model_resources()


def _round_score(value: float) -> float:
    return round(value, 6)


def predict_label_scores(text: str, threshold: float, top_k: int) -> tuple[list[LabelScore], list[LabelScore]]:
    tokenizer, model = get_model_resources()
    encoded = tokenizer(
        text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    with torch.no_grad():
        logits = model(**encoded).logits.squeeze(0)
        probabilities = torch.sigmoid(logits).tolist()

    id2label = model.config.id2label
    scored_labels = [
        LabelScore(label=id2label[idx], score=_round_score(float(score)))
        for idx, score in enumerate(probabilities)
    ]
    scored_labels.sort(key=lambda item: item.score, reverse=True)

    filtered = [item for item in scored_labels if item.score >= threshold][:top_k]
    if not filtered:
        filtered = [scored_labels[0]]

    return filtered, scored_labels


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": MODEL_ID}


@app.post("/api/v1/emotions/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    threshold = payload.threshold if payload.threshold is not None else DEFAULT_THRESHOLD
    top_k = payload.top_k if payload.top_k is not None else DEFAULT_TOP_K

    try:
        labels, all_scores = predict_label_scores(payload.text, threshold, top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return PredictResponse(
        model=MODEL_ID,
        problem_type="multi_label_classification",
        text=payload.text,
        threshold_used=threshold,
        top_k_used=top_k,
        labels=labels,
        top_label=labels[0].label,
        all_scores=all_scores if payload.include_all_scores else None,
    )
