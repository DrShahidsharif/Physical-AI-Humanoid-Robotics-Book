# Feature Specification: RAG-Based Interactive Book Chatbot

**Feature Branch**: `002-rag-chatbot`
**Created**: 2025-01-20
**Status**: Draft
**Input**: User description: "I need to build a RAG-based chatbot for an interactive book. The architecture should be as follows:

Frontend: Embedded Chatbot (Next.js/React) using ChatKit SDK.

Backend: FastAPI.

Database: Neon Serverless Postgres (for metadata/user sessions) and Qdrant Cloud Free Tier (Vector Store).

LLM: OpenRouter API (Accessing models like Claude or GPT).

Embeddings: Qwen Embedding model (via OpenRouter or HuggingFace).

Key Feature: The bot must answer questions based on the entire book OR only on specific text selected by the user.

Please specify the API endpoints needed, the data schema for Neon, and the vector collection structure for Qdrant."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Book Question Answering (Priority: P1)

A reader wants to ask questions about the content of an interactive book and receive accurate, contextually relevant answers based on the book's content. The user can ask general questions about the entire book or select specific text and ask questions related to that specific content.

**Why this priority**: This is the core functionality of the chatbot - providing an interactive Q&A experience that enhances the reading experience by allowing readers to get clarifications and deeper insights from the book content.

**Independent Test**: Can be fully tested by asking questions about book content and verifying that responses are accurate and relevant to the book's content. The feature delivers immediate value by enabling interactive learning from the book.

**Acceptance Scenarios**:

1. **Given** a user is reading an interactive book with the embedded chatbot, **When** the user types a question about the book content, **Then** the chatbot responds with an answer based on the entire book's content.
2. **Given** a user has selected specific text in the book, **When** the user asks a question related to the selected text, **Then** the chatbot responds with an answer focused on the selected text content.

---

### User Story 2 - Context Switching Between Book and Selected Text (Priority: P2)

A reader wants to seamlessly switch between asking questions about the entire book versus specific selected text, with the chatbot understanding the context and providing appropriate responses.

**Why this priority**: This enhances user experience by providing flexibility in how users interact with the book content, allowing for both broad and focused inquiries.

**Independent Test**: Can be tested by switching between general book questions and specific text questions and verifying that the bot correctly uses the appropriate context for each query.

**Acceptance Scenarios**:

1. **Given** a user has previously asked questions about the entire book, **When** the user selects specific text and asks a new question, **Then** the chatbot responds based on the selected text context.
2. **Given** a user has been asking questions about selected text, **When** the user asks a general question without text selection, **Then** the chatbot responds based on the entire book content.

---

### User Story 3 - User Session Persistence (Priority: P3)

A reader wants their conversation history with the chatbot to be preserved across page refreshes and browser sessions, allowing for continued interaction with the book content.

**Why this priority**: This improves user experience by maintaining conversation context, allowing users to return to their questions and continue the dialogue without losing context.

**Independent Test**: Can be tested by starting a conversation, refreshing the page, and verifying that the conversation history is maintained and accessible.

**Acceptance Scenarios**:

1. **Given** a user has an active conversation with the chatbot, **When** the user refreshes the page, **Then** the conversation history is preserved and visible to the user.
2. **Given** a user has interacted with the chatbot in a previous session, **When** the user returns to the book, **Then** the user can access their previous conversation history.

---

### Edge Cases

- What happens when the selected text is very large (e.g., entire chapters)?
- How does the system handle questions when the book content has been updated since the embeddings were created?
- What happens when the vector database is temporarily unavailable during a query?
- How does the system handle very long or complex questions that exceed LLM token limits?
- What happens when multiple users are asking questions simultaneously, potentially overwhelming the LLM API?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat interface embedded in the book reader that allows users to ask questions about book content
- **FR-002**: System MUST support two modes of operation: general book questions and specific text selection questions
- **FR-003**: System MUST retrieve relevant book content using RAG (Retrieval-Augmented Generation) techniques to inform LLM responses
- **FR-004**: System MUST store user session data in Neon Serverless Postgres database to maintain conversation history
- **FR-005**: System MUST store book content embeddings in Qdrant vector database for efficient similarity search
- **FR-006**: System MUST use OpenRouter API to access LLMs like Claude or GPT for generating responses
- **FR-007**: System MUST generate embeddings using Qwen Embedding model for converting text to vector representations
- **FR-008**: System MUST differentiate between general book questions and specific text selection questions based on user input context
- **FR-009**: System MUST preserve user conversation history across sessions for continuity of interaction
- **FR-010**: System MUST handle errors gracefully when external services (LLM API, vector database) are unavailable

*Example of marking unclear requirements:*

- **FR-011**: System MUST handle text selections up to 5,000 characters in length to accommodate reasonable text selections
- **FR-012**: System MUST retain conversation history for 90 days to maintain user context while managing data storage efficiently

### Key Entities *(include if feature involves data)*

- **UserSession**: Represents a user's interaction session with the chatbot, containing conversation history and metadata
- **BookContent**: Represents the book content that has been processed into chunks for embedding and retrieval
- **EmbeddingVector**: Represents the vector representation of book content chunks stored in the vector database
- **ChatMessage**: Represents individual messages in a conversation between the user and the chatbot

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can ask questions about book content and receive relevant answers within 5 seconds in 95% of cases
- **SC-002**: The system correctly distinguishes between general book questions and specific text selection questions with 90% accuracy
- **SC-003**: Users report a 70% improvement in comprehension when using the interactive chatbot compared to reading without it
- **SC-004**: The system maintains conversation context across page refreshes for at least 30 days
- **SC-005**: The chatbot provides accurate answers based on book content with 85% factual accuracy
