# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

The project is structured as a monorepo with the main library at `libs/redis/`. All development commands should be run from `libs/redis/`:

```
cd libs/redis
```

### Testing

- `make test` - Run unit tests
- `make integration_tests` - Run integration tests (requires OPENAI_API_KEY)
- `TEST_FILE=tests/unit_tests/test_specific.py make test` - Run specific test file

### Linting and Formatting

- `make lint` - Run linters (ruff + mypy)
- `make format` - Auto-format code
- `make check_imports` - Validate import structure
- `make spell_check` - Check spelling with codespell

### Dependencies

- `poetry install --with test` - Install unit test dependencies
- `poetry install --with test,test_integration` - Install all test dependencies
- `poetry install --with lint,typing,test,test_integration` - Install all development dependencies

## Architecture

### Core Components

The library provides three main integrations with Redis:

1. **RedisVectorStore** (`vectorstores.py`) - Vector storage and similarity search
2. **RedisCache/RedisSemanticCache** (`cache.py`) - LLM response caching
3. **RedisChatMessageHistory** (`chat_message_history.py`) - Chat message persistence

### Configuration System

All components use the centralized `RedisConfig` class (`config.py`) which provides:
- Multiple initialization patterns (from_kwargs, from_schema, from_yaml, etc.)
- Pydantic-based validation with smart defaults
- Schema management for Redis index structures
- Connection handling (redis_client or redis_url)

Key design patterns:
- Config validates that only one of `index_schema`, `schema_path`, or `metadata_schema` is specified
- `key_prefix` defaults to `index_name` if not provided
- ULID-based default index names for uniqueness

### Vector Store Implementation

`RedisVectorStore` supports multiple vector search algorithms:
- **FLAT** - Brute force exact search
- **HNSW** - Hierarchical Navigable Small World approximate search
- **Generic** - Automatic algorithm selection based on data size

Key features:
- Async and sync interfaces
- Metadata filtering with Redis queries
- Batch operations for performance
- Configurable similarity metrics (cosine, L2, IP)

### Caching Implementation

**RedisCache** - Simple key-value caching with TTL support
**RedisSemanticCache** - Vector-based semantic similarity caching

Both support:
- Configurable TTL (time-to-live)
- Optional semantic similarity threshold
- Batch operations
- Async operations

## Testing Structure

### Unit Tests (`tests/unit_tests/`)
- Mock Redis connections using fakeredis
- Test individual component functionality
- No external dependencies required

### Integration Tests (`tests/integration_tests/`)
- Require actual Redis instance
- Test against real Redis with docker-compose
- Require OpenAI API key for embeddings

### Test Configuration
- `conftest.py` - Shared fixtures and test utilities
- `docker-compose.yml` - Redis setup for integration tests
- Environment variables for API keys and Redis connections

## Development Workflow

### Setup
1. Install Redis locally or use Docker
2. Install poetry: `pip install poetry`
3. Navigate to `libs/redis/` and run `poetry install --with test,test_integration`
4. Set environment variables: `OPENAI_API_KEY`, `REDIS_URL` (optional)

### Making Changes
1. Write tests first (TDD approach)
2. Implement functionality
3. Run `make test` and `make integration_tests`
4. Run `make lint` and `make format`
5. Update documentation if needed

### Common Patterns
- Use `RedisConfig` for all Redis connection management
- Implement both sync and async versions of methods
- Add comprehensive error handling and logging
- Include metadata validation and type hints

## Key Design Decisions

### Configuration Management
- Single source of truth via `RedisConfig`
- Support multiple initialization patterns for flexibility
- Validate mutually exclusive options at config time

### Vector Operations
- Support multiple algorithms (FLAT, HNSW, Generic)
- Configurable similarity metrics
- Batch operations for performance

### Error Handling
- Comprehensive Redis connection error handling
- Validation of vector dimensions and metadata
- Clear error messages for configuration issues

### Performance Optimizations
- Connection pooling via redis-py
- Batch operations for bulk inserts/updates
- Configurable pipeline operations
- Memory-efficient streaming for large datasets