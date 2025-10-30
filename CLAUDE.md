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
uvicorn rag.app:app --reload

# Or use the CLI entry point
rag
```

### Testing
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_llm.py

# Run with verbose output
pytest -v

# Run a specific test function
pytest tests/test_llm.py::test_function_name
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

### Application Structure

The application follows a layered architecture:

1. **Web Layer** (`app.py`): FastAPI application that serves both the web UI and REST API
   - GET `/`: Returns HTML chatbot interface
   - POST `/api/message`: Accepts user queries and returns AI responses

2. **LLM Layer** (`llm.py`): Handles interactions with AWS Bedrock
   - `get_embedding(query)`: Generates embeddings for semantic search
   - `call(query, documents, prompt)`: Invokes LLM with RAG context

3. **Database Layer** (`db.py`): Vector database for document storage and retrieval (placeholder)

4. **Models Layer** (`models.py`): Pydantic models for request/response validation
   - `Query`: Request model with `text` field

### Key Technical Details

- **Templates**: Uses Jinja2 templates stored in `src/rag/templates/`
- **AWS Integration**: Configured to use boto3 for AWS Bedrock API calls
- **Frontend**: Single-page chat interface with vanilla JavaScript (no framework)

### Request Flow

1. User sends message via web interface
2. Frontend POSTs to `/api/message` with JSON payload: `{"message": "user message"}`
3. Backend receives Query model, processes with LLM layer
4. Response returned as JSON: `{"response": "AI response"}`

## Development Notes

- The LLM functions in `llm.py` are currently stub implementations (ellipsis only)
- The database layer (`db.py`) is a placeholder file
- Test data is defined in `tests/test_llm.py` with sample documents about geography
