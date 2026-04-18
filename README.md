# Serinity AI API

Local-first FastAPI microservice for emotion detection using:

- **Model:** `AnasAlokla/multilingual_go_emotions_V1.2`
- **Task:** multi-label classification
- **Input:** journal text content only

## Project structure

```text
app/
  main.py
requirements.txt
.env.example
README.md
```

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API endpoints

### `GET /health`

Response:

```json
{
  "status": "ok",
  "model": "AnasAlokla/multilingual_go_emotions_V1.2"
}
```

### `POST /api/v1/emotions/predict`

Request body:

```json
{
  "text": "I feel tired and overwhelmed today.",
  "threshold": 0.5,
  "top_k": 5,
  "include_all_scores": false
}
```

Rules:

- `text` is required and must not be blank
- `threshold` is optional, float between `0` and `1`
- `top_k` is optional, integer between `1` and `28`
- `include_all_scores` is optional boolean

## curl test example

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/emotions/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel tired and overwhelmed today.",
    "threshold": 0.5,
    "top_k": 5,
    "include_all_scores": false
  }'
```

Expected JSON response shape:

```json
{
  "model": "AnasAlokla/multilingual_go_emotions_V1.2",
  "problem_type": "multi_label_classification",
  "text": "I feel tired and overwhelmed today.",
  "threshold_used": 0.5,
  "top_k_used": 5,
  "labels": [
    { "label": "sadness", "score": 0.81 },
    { "label": "nervousness", "score": 0.67 }
  ],
  "top_label": "sadness",
  "all_scores": null
}
```

## Sample journal texts

- **English:** `I feel tired and overwhelmed today.`
- **French:** `Je me sens épuisé et anxieux aujourd'hui.`
- **Arabic:** `أشعر بالإرهاق والتوتر اليوم.`

## Environment variables

- `MODEL_ID` (default: `AnasAlokla/multilingual_go_emotions_V1.2`)
- `DEFAULT_THRESHOLD` (default: `0.5`)
- `DEFAULT_TOP_K` (default: `5`)
- `MAX_LENGTH` (default: `256`)

## Notes for future deployment

This FastAPI app is container-friendly and can later be deployed to a Hugging Face Docker Space without changing the API contract.
