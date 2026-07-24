# Repository Root Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 6 project files.

## .env.example

**File path:** `.env.example`

```
# Copy this file to .env and replace the placeholder with your Gemini API key.
# Never commit the real .env file.
GEMINI_API_KEY_1=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-3.6-flash
```

## .gitignore

**File path:** `.gitignore`

```
.env
*.env

__pycache__/
*.pyc

.venv/
venv/

.streamlit/
```

## README.md

**File path:** `README.md`

````markdown
# NIBS-Hackathon-2026
Hackathon 2026

## Gemini setup

The AI Assistant uses the existing RAG-backed KnowledgeAgent, which requires a
Gemini API key. Create a local configuration file before using the assistant:

```powershell
Copy-Item .env.example .env
```

Then replace `YOUR_GEMINI_API_KEY_HERE` in `.env` with a real Gemini API key.
The `.env` file is ignored by Git and must not be committed.

The application loads the repository-root `.env` automatically and supports
these environment variable names: `GEMINI_API_KEY_1` (preferred),
`GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_KEY_1`.

The default production model is `gemini-3.6-flash`. Set `GEMINI_MODEL` in
`.env` only when you need to select another model available to your Gemini API
project.
````

## alembic.ini

**File path:** `alembic.ini`

```ini
[alembic]
script_location = database/migrations
prepend_sys_path = .

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

## requirements.txt

**File path:** `requirements.txt`

```
# UI
streamlit
# API
fastapi
uvicorn
# Database
sqlalchemy
psycopg2-binary
pgvector
# Environment / config
python-dotenv
# Validation
pydantic
# Logging
loguru
agno
llama-index
# Vector databases
chromadb
# Embeddings
sentence-transformers
# Google Gemini
google-generativeai
langchain-google-genai
# OpenAI fallback
openai
langchain-openai
# LangChain core
langchain
langchain-community
langchain-huggingface
# PDF loading
pypdf
# FAISS vector store
faiss-cpu
# Utilities
uuid64
streamlit
plotly
pandas
python-dotenv
requests
sqlalchemy
psycopg2-binary
pgvector
langchain
langchain-community
langchain-google-genai
sentence-transformers
faiss-cpu
pypdf
# Streamlit UI and domain models
streamlit==1.59.2
pydantic==2.13.4
python-dotenv==1.2.2
# PostgreSQL persistence
SQLAlchemy==2.0.51
alembic==1.18.5
psycopg2-binary==2.9.12
pgvector==0.5.0
# Retrieval-augmented knowledge agent
langchain-community==0.4.2
langchain-google-genai==4.2.7
langchain-huggingface==1.2.2
langchain-text-splitters==1.1.2
sentence-transformers==5.6.0
transformers==5.14.1
torch==2.13.0
faiss-cpu==1.14.3
pypdf==6.14.2
alembic
torchvision
```

## run.py

**File path:** `run.py`

```python

```
