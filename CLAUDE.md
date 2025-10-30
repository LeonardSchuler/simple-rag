# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) chatbot application built with FastAPI and AWS Bedrock. The project uses `uv` for dependency management and requires Python 3.13+.

## Development Commands

### Environment Setup
```bash
# Install dependencies (including dev dependencies)
uv sync --all-groups

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
```

### Running the Application
```bash
# Run the FastAPI development server
uvicorn rag.app.main:app --reload

# Or use the CLI entry point
rag
```

### Testing
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v
```

### Dependency Management
```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv sync
```

## Architecture

This project implements **Hexagonal Architecture (Ports & Adapters)** with clear separation between business logic, infrastructure, and application layers.

### Directory Structure

```
src/rag/
├── core/          # Business logic (domain layer)
│   ├── ports.py      # Protocol interfaces defining contracts
│   └── services.py   # Core RAG orchestration logic
├── adapters/      # Infrastructure implementations
│   ├── db.py                # Vector database adapters (EmptyDB stub)
│   └── language_models.py   # LLM adapters (Parrot stub)
└── app/           # FastAPI web layer
    ├── main.py          # FastAPI app and routes
    ├── models.py        # Pydantic request/response models
    ├── dependencies.py  # Dependency injection configuration
    └── templates/       # HTML templates
```

### Hexagonal Architecture Layers

**Core (src/rag/core/):**
- `ports.py` defines Protocol interfaces (VectorDatabase, LanguageModel, MessageService)
- `services.py` contains MessageService which orchestrates the RAG workflow:
  1. Get embedding of user message
  2. Search for similar documents in vector store
  3. Retrieve documents corresponding to similar embeddings
  4. Pass message + context to LLM for generation
- Core has ZERO dependencies on external frameworks or AWS

**Adapters (src/rag/adapters/):**
- Implement the port interfaces from core
- Current implementations are stubs for development:
  - `EmptyDB`: Returns empty embeddings (replace with Bedrock Knowledge Base)
  - `Parrot`: Echoes input (replace with Bedrock Claude models)
- Future AWS Bedrock integration happens here via boto3

**Application (src/rag/app/):**
- `main.py`: FastAPI routes (GET / for UI, POST /api/message for chat)
- `dependencies.py`: Dependency injection that wires adapters to core services
- `models.py`: Pydantic schemas for HTTP requests/responses

### Dependency Injection Pattern

The app uses constructor-based dependency injection via FastAPI's `Depends`:

```python
# Core service depends on port interfaces, not implementations
@dataclass
class MessageService:
    vector_db: ports.VectorDatabase
    language_model: ports.LanguageModel

# FastAPI provides concrete implementations
def get_message_service(
    vector_db: Annotated[ports.VectorDatabase, Depends(get_database)],
    language_model: Annotated[ports.LanguageModel, Depends(get_language_model)],
) -> ports.MessageService:
    return services.MessageService(vector_db=vector_db, language_model=language_model)
```

This design enables:
- Easy swapping of implementations (stub → real AWS services)
- Simple mocking for tests
- Core logic remains independent of infrastructure

### RAG Data Flow

```
User Message → FastAPI → MessageService → VectorDatabase.get_embedding()
                                       → VectorDatabase.search_similar()
                                       → VectorDatabase.inverse_embeddings()
                                       → LanguageModel.answer(message, context)
                                       → Response
```

### AWS Bedrock Integration Points

Currently stubbed but designed for AWS Bedrock integration:

1. **Vector Database (adapters/db.py):** Replace EmptyDB with Bedrock Knowledge Base or embeddings API
2. **Language Model (adapters/language_models.py):** Replace Parrot with Bedrock Claude models via boto3
3. AWS credentials: Use standard boto3 configuration (environment variables, ~/.aws/credentials, or IAM roles)

### Testing Strategy

- Tests use FastAPI's `TestClient` with dependency overrides
- `app.dependency_overrides` injects stub implementations to avoid external calls
- Run individual tests: `pytest tests/test_app.py -k test_name`
- Tests demonstrate the dependency injection pattern in action

### Key Design Principles

- **Ports & Adapters:** Domain logic isolated from frameworks
- **Protocol (Structural Typing):** Python 3.13 Protocol classes define contracts
- **Dependency Injection:** Loose coupling between layers
- **Repository Pattern:** VectorDatabase abstracts data persistence
- **Service Layer:** MessageService orchestrates business logic

### Extending the Application

To add real AWS Bedrock integration:

1. Create new adapter classes in `adapters/` that implement the port interfaces
2. Update `dependencies.py` to return the new adapters instead of stubs
3. Configure boto3 with AWS credentials
4. Core business logic in `services.py` remains unchanged
