# Implementation Tasks: RAG-Based Interactive Book Chatbot

**Feature**: RAG-Based Interactive Book Chatbot
**Branch**: `002-rag-chatbot`
**Generated**: 2025-01-20
**Spec**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

## Implementation Strategy

The implementation will follow a phased approach, starting with the most critical user story (P1) to deliver an MVP, then incrementally adding features for P2 and P3 stories. The strategy prioritizes delivering core functionality first, with foundational infrastructure established early.

**MVP Scope**: User Story 1 (Book Question Answering) with basic general questions functionality, sufficient to test the core RAG pipeline.

## Phase 1: Setup

**Goal**: Establish project structure and configure external services

- [X] T001 Create backend directory structure per plan
- [ ] T002 Create frontend directory structure per plan
- [X] T003 Setup Python virtual environment and requirements.txt
- [ ] T004 Setup Node.js package.json for frontend
- [X] T005 Create .env file templates for backend and frontend
- [X] T006 Install core dependencies (FastAPI, Qdrant client, OpenAI, etc.)
- [X] T007 Configure basic FastAPI application structure
- [ ] T008 Setup basic Next.js/React project structure

## Phase 2: Foundational Infrastructure

**Goal**: Establish core services and database connections needed by all user stories

- [X] T009 [P] Configure settings module with environment variables (OpenRouter Key, Qdrant URL, Neon URL)
- [ ] T010 [P] Implement database connection module for Neon Postgres
- [X] T011 [P] Implement Qdrant client configuration module
- [X] T012 [P] Create OpenRouter API utility function for chat completions
- [X] T013 [P] Implement Qwen embedding generation utility using OpenRouter API
- [ ] T014 [P] Create base models for UserSession, ChatMessage, and BookContent
- [ ] T015 [P] Implement session management service with Neon Postgres
- [ ] T016 [P] Create basic API error handling and middleware

## Phase 3: User Story 1 - Book Question Answering (P1)

**Goal**: Enable users to ask questions about the entire book content and receive accurate, contextually relevant answers

**Independent Test Criteria**: Can ask questions about book content and verify responses are accurate and relevant to the book's content

- [ ] T017 [P] [US1] Create BookContent model in src/models/book_content.py
- [ ] T018 [P] [US1] Create EmbeddingVector model in src/models/embedding_vector.py
- [X] T019 [P] [US1] Implement embedding service to process book content in src/services/embedding_service.py
- [X] T020 [P] [US1] Implement Qdrant service for vector storage in src/services/qdrant_service.py
- [X] T021 [P] [US1] Write script to process book PDF/Markdown, chunk it, and upload to Qdrant using Qwen embeddings in scripts/process_book.py
- [X] T022 [P] [US1] Implement RAG service for general book questions in src/services/rag_service.py
- [X] T023 [US1] Create /ask endpoint in src/api/routes/ask.py
- [X] T024 [P] [US1] Implement text selection RAG functionality in src/services/rag_service.py
- [X] T025 [US1] Create /ask-selection endpoint in src/api/routes/ask_selection.py
- [ ] T026 [P] [US1] Implement frontend ChatBot component using ChatKit SDK in frontend/src/components/ChatBot.jsx
- [ ] T027 [P] [US1] Implement BookReader component in frontend/src/components/BookReader.jsx
- [ ] T028 [P] [US1] Create API service for frontend-backend communication in frontend/src/services/api.js
- [ ] T029 [US1] Integrate frontend components with backend API endpoints
- [ ] T030 [US1] Test complete user flow: question → RAG → answer

## Phase 4: User Story 2 - Context Switching (P2)

**Goal**: Enable seamless switching between asking questions about the entire book versus specific selected text

**Independent Test Criteria**: Can switch between general book questions and specific text questions and verify the bot correctly uses the appropriate context for each query

- [ ] T031 [P] [US2] Enhance RAG service with context switching logic
- [ ] T032 [P] [US2] Implement context tracking in session management
- [ ] T033 [US2] Update /ask endpoint to handle context switching
- [ ] T034 [US2] Update /ask-selection endpoint to handle context switching
- [ ] T035 [P] [US2] Implement TextSelectionHandler component in frontend/src/components/TextSelectionHandler.jsx
- [ ] T036 [P] [US2] Create text selection utility in frontend/src/utils/textExtractor.js
- [ ] T037 [US2] Update frontend to properly pass context to backend endpoints
- [ ] T038 [US2] Test context switching functionality between question types

## Phase 5: User Story 3 - User Session Persistence (P3)

**Goal**: Preserve conversation history across page refreshes and browser sessions

**Independent Test Criteria**: Can start a conversation, refresh the page, and verify conversation history is maintained and accessible

- [ ] T039 [P] [US3] Enhance UserSession model with retention logic
- [ ] T040 [P] [US3] Implement session persistence service in src/services/session_service.py
- [ ] T041 [P] [US3] Add session history retrieval to session management
- [ ] T042 [P] [US3] Implement frontend session management in frontend/src/services/sessionService.js
- [ ] T043 [US3] Add session persistence to frontend components
- [ ] T044 [US3] Implement session cleanup for retention policy (90 days)
- [ ] T045 [US3] Test session persistence across page refreshes and browser sessions

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Add error handling, validation, and quality improvements

- [ ] T046 [P] Add comprehensive input validation for all API endpoints
- [ ] T047 [P] Implement error handling for external service unavailability (OpenRouter, Qdrant)
- [ ] T048 [P] Add rate limiting and request throttling
- [ ] T049 [P] Implement comprehensive logging for debugging
- [ ] T050 [P] Add unit tests for backend services
- [ ] T051 [P] Add integration tests for API endpoints
- [ ] T052 [P] Add frontend component tests
- [ ] T053 [P] Optimize response times to meet 5-second requirement
- [ ] T054 [P] Add documentation for API endpoints
- [ ] T055 [P] Implement caching for frequently asked questions

## Dependencies

- **User Story 2** depends on: User Story 1 (core RAG functionality must exist first)
- **User Story 3** depends on: User Story 1 (session management builds on basic functionality)

## Parallel Execution Examples

**User Story 1 Parallel Tasks**:
- T017-T020: Model and service implementations (different files, no dependencies)
- T026-T028: Frontend component development (independent of backend implementation)
- T021, T023, T025: Script and endpoint creation (different modules)

**User Story 2 Parallel Tasks**:
- T031-T032: Backend context switching enhancements
- T035-T036: Frontend text selection components

**User Story 3 Parallel Tasks**:
- T039-T041: Backend session persistence
- T042-T043: Frontend session management