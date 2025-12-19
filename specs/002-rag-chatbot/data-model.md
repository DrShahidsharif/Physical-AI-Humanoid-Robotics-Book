# Data Model: RAG-Based Interactive Book Chatbot

## Entity: UserSession

**Description**: Represents a user's interaction session with the chatbot, containing conversation history and metadata

**Fields**:
- `session_id` (string): Unique identifier for the session
- `created_at` (datetime): Timestamp when session was created
- `last_active` (datetime): Timestamp of last activity in session
- `conversation_history` (JSON): Array of chat messages in the session
- `user_id` (string, optional): Identifier for authenticated user
- `book_id` (string): Identifier for the book being read

**Validation Rules**:
- `session_id` must be unique
- `created_at` must be in the past
- `last_active` must be >= `created_at`
- `conversation_history` must not exceed size limits

## Entity: ChatMessage

**Description**: Represents individual messages in a conversation between the user and the chatbot

**Fields**:
- `message_id` (string): Unique identifier for the message
- `session_id` (string): Reference to the parent session
- `role` (string): Message role (either "user" or "assistant")
- `content` (string): The actual message content
- `timestamp` (datetime): When the message was created
- `metadata` (JSON, optional): Additional message metadata

**Validation Rules**:
- `message_id` must be unique
- `role` must be either "user" or "assistant"
- `content` must not exceed character limits
- `session_id` must reference an existing session

## Entity: BookContent

**Description**: Represents the book content that has been processed into chunks for embedding and retrieval

**Fields**:
- `content_id` (string): Unique identifier for the content chunk
- `book_id` (string): Identifier for the book
- `text_chunk` (string): The actual text content
- `chunk_index` (integer): Position of this chunk in the book sequence
- `page_number` (integer, optional): Page number reference
- `embedding_vector` (array): The vector representation of the text
- `metadata` (JSON): Additional content metadata

**Validation Rules**:
- `content_id` must be unique
- `text_chunk` must not exceed size limits
- `chunk_index` must be non-negative
- `embedding_vector` must have correct dimensions (1536 for Qwen)

## Entity: EmbeddingVector

**Description**: Represents the vector representation of book content chunks stored in the vector database (Qdrant)

**Fields**:
- `vector_id` (string): Unique identifier matching the content_id
- `vector_data` (array): The actual embedding vector (1536 dimensions)
- `book_id` (string): Reference to the book
- `payload` (JSON): Additional data for retrieval
  - `text_chunk`: Original text
  - `chunk_index`: Position in book
  - `page_number`: Page reference

**Validation Rules**:
- `vector_id` must match a content_id in BookContent
- `vector_data` must have exactly 1536 dimensions
- `payload` must contain required fields

## Relationships

### UserSession → ChatMessage
- **Type**: One-to-Many
- **Description**: A session contains multiple chat messages
- **Constraint**: Messages are deleted when session is deleted

### BookContent → EmbeddingVector
- **Type**: One-to-One
- **Description**: Each content chunk has one corresponding embedding vector
- **Constraint**: Both entities must exist together

## State Transitions

### UserSession
- `created` → `active` (when first message is sent)
- `active` → `inactive` (when session expires or user logs out)
- `inactive` → `archived` (when retention period expires)

## Indexes

### UserSession
- Index on `session_id` (primary)
- Index on `last_active` (for session cleanup)
- Index on `user_id` (for user session retrieval)

### ChatMessage
- Index on `message_id` (primary)
- Index on `session_id` (for session message retrieval)
- Index on `timestamp` (for chronological ordering)

### BookContent
- Index on `content_id` (primary)
- Index on `book_id` (for book content retrieval)
- Index on `chunk_index` (for sequential access)