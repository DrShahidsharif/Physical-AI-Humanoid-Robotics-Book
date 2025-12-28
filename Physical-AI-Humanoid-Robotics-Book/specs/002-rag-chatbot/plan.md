# Implementation Plan: RAG-Based Interactive Book Chatbot

**Branch**: `002-rag-chatbot` | **Date**: 2025-01-20 | **Spec**: [link to spec](../spec.md)
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a RAG-based chatbot for interactive books with dual-mode operation (entire book vs. specific text selection). The system will use FastAPI backend with Qdrant vector storage, Neon Postgres for session management, and OpenRouter API for LLM responses with Qwen embeddings. The plan covers data ingestion, vector storage setup, backend development with dual endpoints, RAG logic implementation, and frontend text selection integration.

## Technical Context

**Language/Version**: Python 3.11 (backend), Node.js 18+ (frontend)
**Primary Dependencies**: FastAPI, Qdrant, Neon Postgres, OpenRouter API, Qwen Embeddings, Next.js/React, ChatKit SDK
**Storage**: Neon Serverless Postgres (session data), Qdrant Cloud (vector embeddings)
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Next.js/React frontend with FastAPI backend)
**Project Type**: Web
**Performance Goals**: 95% of queries respond within 5 seconds, 90% accuracy in distinguishing question types
**Constraints**: <5000 char text selection limit, <5s p95 response time, <90 days session retention
**Scale/Scope**: Single web application supporting multiple books, concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Accuracy and Verifiability**: All technical decisions will be based on official documentation for Qdrant, FastAPI, Neon Postgres, and OpenRouter API
- **Clarity and Accessibility**: Implementation will follow clear patterns suitable for beginner-intermediate developers
- **Reproducibility**: All steps will be fully reproducible with clear setup instructions
- **Best Practices for AI Writing & SSG**: Following standard RAG implementation patterns and FastAPI best practices
- **Traceable and Cited Claims**: All technical choices will reference official documentation
- **Writing Clarity and Consistency**: Documentation will maintain consistent structure

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user_session.py
│   │   ├── chat_message.py
│   │   └── book_content.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── rag_service.py
│   │   ├── qdrant_service.py
│   │   └── openrouter_service.py
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── ask.py
│   │   │   └── ask_selection.py
│   │   └── dependencies.py
│   └── config/
│       ├── database.py
│       └── settings.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatBot.jsx
│   │   ├── BookReader.jsx
│   │   └── TextSelectionHandler.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── textSelection.js
│   ├── pages/
│   │   └── BookPage.jsx
│   └── utils/
│       └── textExtractor.js
└── tests/
```

**Structure Decision**: Selected web application structure with separate backend and frontend directories to accommodate the specified architecture (FastAPI backend with Next.js/React frontend).

## Phase 0: Research & Analysis

### Data Ingestion Research
- **Decision**: Use Qwen embedding model via OpenRouter API for generating embeddings
- **Rationale**: Qwen embeddings are specifically requested in the feature spec and provide good performance for text similarity
- **Alternatives considered**: HuggingFace transformers, OpenAI embeddings, local embedding models
- **Chunking strategy**: Text will be chunked into 512-1024 token segments with 10% overlap to maintain context

### Vector Storage Research
- **Decision**: Use Qdrant Cloud Free Tier with cosine similarity distance
- **Rationale**: Qdrant is specifically requested in the feature spec and provides efficient similarity search
- **Qwen embedding dimensions**: 1536 dimensions (based on Qwen model specifications)
- **Collection structure**: One collection per book with metadata for context tracking

### Backend Development Research
- **Decision**: FastAPI with two distinct endpoints (/ask for general questions, /ask-selection for specific text)
- **Rationale**: Clear separation of concerns for different question contexts
- **RAG pipeline**: Retrieve → Augment → Generate pattern with proper context switching

### Frontend Integration Research
- **Decision**: Use text selection APIs and ChatKit SDK for seamless integration
- **Rationale**: Provides best user experience for selecting text and asking questions
- **Implementation**: Event listeners for text selection with context passing to backend

## Phase 1: Design & Contracts

### API Contracts
1. **POST /ask** - General book questions
   - Request: { question: string, session_id: string }
   - Response: { answer: string, sources: string[] }

2. **POST /ask-selection** - Specific text questions
   - Request: { question: string, selected_text: string, session_id: string }
   - Response: { answer: string, sources: string[] }

### Data Models
- **UserSession**: session_id, created_at, last_active, conversation_history
- **ChatMessage**: message_id, session_id, role, content, timestamp
- **BookContent**: content_id, book_id, text_chunk, embedding_vector, metadata

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple external services | Required for RAG functionality | Single service approach insufficient for vector storage + LLM + session management |
| Dual API endpoints (/ask and /ask-selection) | Required for different question modes | Single endpoint insufficient for handling different contexts properly |
| Complex RAG pipeline | Required for accurate book-based answers | Simpler approaches would not provide contextually relevant responses |
