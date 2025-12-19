# Research: RAG-Based Interactive Book Chatbot

## Data Ingestion: Book Content Chunking and Qwen Embeddings

### Decision: Use Qwen embedding model via OpenRouter API
- **Rationale**: Qwen embeddings are specifically requested in the feature spec and provide good performance for text similarity tasks
- **Alternatives considered**:
  1. HuggingFace transformers - Requires local model hosting and management
  2. OpenAI embeddings - Not specified in requirements, potential cost concerns
  3. Local embedding models - More complex deployment, not requested

### Chunking Strategy
- **Approach**: Text will be chunked into 512-1024 token segments with 10% overlap
- **Rationale**: Maintains context while keeping embedding quality high
- **Implementation**: Use recursive character text splitter with overlap to preserve context across chunks

### Qwen Embedding Dimensions
- **Dimensions**: 1536 dimensions (based on Qwen model specifications)
- **Reference**: Qwen models typically use 1536 dimensions for their embedding space

## Vector Storage: Qdrant Collection Setup

### Decision: Use Qdrant Cloud Free Tier with cosine similarity
- **Rationale**: Qdrant is specifically requested in the feature spec and provides efficient similarity search
- **Alternatives considered**:
  1. Pinecone - Not specified in requirements
  2. Weaviate - Not specified in requirements
  3. Local Qdrant - More complex deployment

### Collection Structure
- **Schema**: One collection per book with metadata for context tracking
- **Fields**:
  - `id`: Unique identifier for the chunk
  - `vector`: 1536-dimensional embedding vector
  - `payload`:
    - `text_chunk`: Original text
    - `book_id`: Identifier for the book
    - `chunk_index`: Position in the book
    - `page_number`: Page reference (if applicable)

### Qdrant Configuration
- **Distance metric**: Cosine similarity
- **Indexing**: HNSW with product quantization for efficiency
- **Replication**: Not needed for free tier, but considered for production

## Backend Development: FastAPI Routes

### Decision: Two distinct endpoints for different question modes
- **Rationale**: Clear separation of concerns for different question contexts
- **Endpoints**:
  1. `POST /ask` - General book questions
  2. `POST /ask-selection` - Specific text questions

### FastAPI Implementation Considerations
- **Dependencies**: Pydantic for request/response validation
- **Middleware**: Rate limiting and authentication (if needed)
- **Error handling**: Graceful fallback when external services are unavailable

## RAG Logic: Retrieval Pipeline

### Decision: Retrieve → Augment → Generate pattern
- **Rationale**: Standard RAG pattern that provides contextually relevant responses
- **Process**:
  1. **Retrieve**: Search Qdrant for relevant text chunks based on query
  2. **Augment**: Combine retrieved context with user query
  3. **Generate**: Call OpenRouter API to generate response

### Context Switching Logic
- **General questions**: Search entire book content
- **Specific text questions**: Search only within selected text context
- **Implementation**: Different query strategies based on endpoint used

## Frontend Integration: Text Selection Capture

### Decision: Use browser text selection APIs with ChatKit SDK
- **Rationale**: Provides best user experience for selecting text and asking questions
- **Implementation**:
  1. Event listeners for text selection
  2. Integration with ChatKit SDK for chat interface
  3. Context passing to backend endpoints

### Text Selection Handling
- **API**: window.getSelection() or similar
- **Validation**: Ensure selection is within book content
- **Limiting**: Cap at 5000 characters as specified in requirements

## Technology Stack Validation

### FastAPI Backend
- **Benefits**: High performance, automatic API documentation, async support
- **Integration**: Easy integration with Qdrant and OpenRouter APIs

### Qdrant Vector Database
- **Benefits**: Efficient similarity search, cloud hosting available, good Python SDK
- **Integration**: Direct Python client for backend services

### OpenRouter API
- **Benefits**: Access to multiple LLMs (Claude, GPT), managed service
- **Integration**: Standard OpenAI-compatible API calls

### Neon Postgres
- **Benefits**: Serverless, easy scaling, familiar SQL interface
- **Use case**: User session management and conversation history

## Performance and Scalability Considerations

### Response Time Goals
- **Target**: 95% of queries respond within 5 seconds
- **Optimization**: Caching frequently asked questions, efficient vector search

### Session Management
- **Retention**: 90 days as specified in requirements
- **Storage**: Neon Postgres for structured session data