# RAG Chatbot Backend

A complete RAG (Retrieval-Augmented Generation) chatbot backend built with FastAPI, using OpenRouter for LLM, Qdrant for vector storage, and in-memory storage for logging.

## Features

- FastAPI backend with async support
- Qdrant vector database for document retrieval
- OpenRouter integration with Qwen model
- In-memory chat history logging (with option for Neon Postgres)
- Support for both general questions and specific text selection
- Mock embedding service for testing without API keys

## Tech Stack

- **Framework**: FastAPI
- **LLM**: OpenRouter (Qwen/qwen-2.5-72b-instruct)
- **Embeddings**: OpenRouter embeddings (with mock fallback)
- **Vector Store**: Qdrant (cloud or local)
- **Database**: In-memory storage (with option for Neon Postgres)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```bash
# Get your OpenRouter API key from https://openrouter.ai/keys
OPENROUTER_API_KEY=your_actual_api_key_here

# Qdrant configuration - get from your Qdrant Cloud dashboard or use localhost:6333 for local
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Neon Postgres configuration - get from your Neon dashboard (optional)
NEON_DATABASE_URL=your_neon_database_url_here
```

3. Create a `book.txt` file with your book content, or use the sample one provided.

## Usage

### 1. Ingest Book Data
```bash
python ingest.py
```
This will:
- Create a Qdrant collection named "book_data"
- Read book.txt, chunk it into 500-character pieces
- Generate embeddings and upload to Qdrant
- If Qdrant is not available, it will show a message but continue

### 2. Run the API Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Use the API

**Endpoint**: `POST /ask`

**Request Body**:
```json
{
  "question": "Your question here",
  "selected_text": "Optional selected text (if provided, this will be used as context instead of vector search)"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "selected_text": "Optional text to use as context"
  }'
```

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /ask` - Ask questions with optional selected text

## Architecture

The system works as follows:
1. If `selected_text` is provided, use it directly as context
2. Otherwise, generate embedding for the question and search Qdrant for similar content
3. Combine relevant results as context
4. Send context + question to Qwen model via OpenRouter
5. Log the interaction to in-memory storage
6. Return the response

## Testing Without API Keys

The system includes mock functionality for testing:
- If OPENROUTER_API_KEY starts with "sk-" or is not set, mock embeddings are used
- If Qdrant is not available, the system continues with empty search results
- This allows you to test the overall flow without external dependencies