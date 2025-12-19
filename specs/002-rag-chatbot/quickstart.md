# Quickstart Guide: RAG-Based Interactive Book Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Access to OpenRouter API (for LLM access)
- Qdrant Cloud account (for vector storage)
- Neon Postgres account (for session storage)

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_postgres_connection_string
```

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn qdrant-client openai psycopg2-binary python-dotenv
   ```

3. Start the backend server:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### General Book Questions
- **Endpoint**: `POST /ask`
- **Description**: Ask questions about the entire book content
- **Request Body**:
  ```json
  {
    "question": "Your question here",
    "session_id": "session_identifier"
  }
  ```

### Specific Text Questions
- **Endpoint**: `POST /ask-selection`
- **Description**: Ask questions about specific selected text
- **Request Body**:
  ```json
  {
    "question": "Your question here",
    "selected_text": "The text that was selected",
    "session_id": "session_identifier"
  }
  ```

## Data Ingestion

To populate the vector database with book content:

1. Prepare your book content as text chunks
2. Use the embedding service to generate Qwen embeddings
3. Store the embeddings in Qdrant with appropriate metadata

Example script for data ingestion:
```python
from src.services.embedding_service import generate_embeddings
from src.services.qdrant_service import store_embeddings

# Load book content
book_content = load_book_content("path/to/book.txt")

# Generate embeddings
embeddings = generate_embeddings(book_content)

# Store in Qdrant
store_embeddings(embeddings, book_id="book_123")
```

## Frontend Integration

The frontend includes a text selection handler that captures selected text and sends it to the appropriate backend endpoint. The ChatKit SDK is integrated for the chat interface.

## Testing

Run backend tests:
```bash
pytest tests/
```

Run frontend tests:
```bash
npm test
```

## Deployment

1. Set up production environment variables
2. Deploy backend to a cloud provider (e.g., Heroku, AWS, GCP)
3. Deploy frontend to a static hosting service (e.g., Vercel, Netlify)
4. Ensure all external services (Qdrant, Neon, OpenRouter) are properly configured