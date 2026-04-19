<!-- PROJECT SHIELDS -->
<p align="center">
  <img src="https://img.shields.io/github/stars/Gl3diator/serinity-ai-api?style=for-the-badge">
  <img src="https://img.shields.io/github/forks/Gl3diator/serinity-ai-api?style=for-the-badge">
  <img src="https://img.shields.io/github/issues/Gl3diator/serinity-ai-api?style=for-the-badge">
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
</p>

<h1 align="center">Serinity AI API</h1>
<p align="center">
  Local-first FastAPI microservice for multilingual emotion detection
</p>

---

<!-- PROJECT LINKS -->
<p align="center">
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#local-setup">Local Setup</a> •
  <a href="#docker-setup">Docker Setup</a> •
  <a href="#api-endpoints">API Endpoints</a>
</p>

Local-first FastAPI microservice for emotion detection using:

- **Model:** `AnasAlokla/multilingual_go_emotions_V1.2`
- **Task:** multi-label classification
- **Input:** journal text content only

## Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Uvicorn-ASGI-4051B5?style=for-the-badge&logo=uvicorn&logoColor=white">
  <img src="https://img.shields.io/badge/Transformers-Hugging%20Face-FFB000?style=for-the-badge&logo=huggingface&logoColor=white">
  <img src="https://img.shields.io/badge/PyTorch-CPU-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white">
</p>

## Project Structure

```text
app/
  main.py
requirements.txt
.env.example
README.md
run-local-ai.sh          (Linux/macOS)
run-local-ai.bat         (Windows CMD)
run-local-ai.ps1         (Windows PowerShell)
```

## Prerequisites

### Linux/macOS
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Windows
- Python 3.11 or higher (download from [python.org](https://www.python.org/downloads/))
  - ⚠️ **Important:** Check "Add Python to PATH" during installation
- pip (included with Python)
- Git (optional, from [git-scm.com](https://git-scm.com/downloads))

## Local setup

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./run-local-ai.sh
```

Or run manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
.\run-local-ai.ps1
```

Or run manually:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Windows (CMD)

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
.\run-local-ai.bat
```

Or run manually:
```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Docker setup

### Linux/macOS

```bash
cp .env.example .env
docker build -t serinity-ai-api:latest .
docker run --rm --name serinity-ai-api --env-file .env -p 8000:8080 serinity-ai-api:latest
```

### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
docker build -t serinity-ai-api:latest .
docker run --rm --name serinity-ai-api --env-file .env -p 8000:8080 serinity-ai-api:latest
```

### Windows (CMD)

```bat
copy .env.example .env
docker build -t serinity-ai-api:latest .
docker run --rm --name serinity-ai-api --env-file .env -p 8000:8080 serinity-ai-api:latest
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
