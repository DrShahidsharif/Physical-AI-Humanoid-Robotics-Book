# RAG-Based Interactive Book Chatbot - Backend

This is the backend component of the RAG-based interactive book chatbot built with FastAPI.

## Features

- RAG (Retrieval-Augmented Generation) system for book content
- Support for both general book questions and specific text selection questions
- Vector storage using Qdrant for efficient similarity search
- LLM integration via OpenRouter API
- Proper system prompting to maintain "book assistant" character

## Architecture

- **FastAPI**: Web framework for API endpoints
- **Qdrant**: Vector database for book content embeddings
- **OpenRouter**: LLM access for generating responses
- **Embedding Service**: Generates embeddings using Qwen-compatible models

## Endpoints

### POST /api/v1/query
Main query endpoint that accepts:
- `user_question`: The question to ask
- `selected_text` (optional): Specific text selected by user (if provided, uses this directly as context)
- `book_id` (optional): ID of the book being queried
- `session_id` (optional): User session identifier

### POST /api/v1/ask
For general questions about the entire book:
- `question`: The question to ask about the book
- `session_id`: User session identifier
- `book_id` (optional): ID of the book being queried

### POST /api/v1/ask-selection
For questions about specific selected text:
- `question`: The question about selected text
- `selected_text`: The text that was selected
- `session_id`: User session identifier

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Update `.env` with your API keys and configuration

4. Run the application:
```bash
python -m src.api.main
```

## Processing Books

To add a book to the system:

```bash
python scripts/process_book.py --book-path path/to/book.txt --book-id my_book_id
```

This will:
1. Read the book content
2. Chunk the text appropriately
3. Generate embeddings for each chunk
4. Store the embeddings in Qdrant