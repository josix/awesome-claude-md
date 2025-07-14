# Semantic Workbench Developer Guidelines

## AI Context System

**Generate comprehensive codebase context for development:**

- `make ai-context-files` - Generate AI context files for all components
- Files created in `ai_context/generated/` organized by logical boundaries:
  - **Python Libraries** (by functional group):
    - `PYTHON_LIBRARIES_CORE.md` - Core API model, assistant framework, events
    - `PYTHON_LIBRARIES_AI_CLIENTS.md` - Anthropic, OpenAI, LLM clients
    - `PYTHON_LIBRARIES_EXTENSIONS.md` - Assistant/MCP extensions, content safety
    - `PYTHON_LIBRARIES_SPECIALIZED.md` - Guided conversation, assistant drive
    - `PYTHON_LIBRARIES_SKILLS.md` - Skills library with patterns and routines

  - **Assistants** (by individual implementation):
    - `ASSISTANTS_OVERVIEW.md` - Common patterns and all assistant summaries
    - `ASSISTANT_PROJECT.md` - Project assistant (most complex)
    - `ASSISTANT_DOCUMENT.md` - Document processing assistant
    - `ASSISTANT_CODESPACE.md` - Development environment assistant
    - `ASSISTANT_NAVIGATOR.md` - Workbench navigation assistant
    - `ASSISTANT_PROSPECTOR.md` - Advanced agent with artifact creation
    - `ASSISTANTS_OTHER.md` - Explorer, guided conversation, skill assistants

  - **Platform Components**:
    - `WORKBENCH_FRONTEND.md` - React app components and UI patterns
    - `WORKBENCH_SERVICE.md` - Backend API, database, and service logic
    - `MCP_SERVERS.md` - Model Context Protocol server implementations
    - `DOTNET_LIBRARIES.md` - .NET libraries and connectors

  - **Supporting Files**:
    - `EXAMPLES.md` - Sample code and getting-started templates
    - `TOOLS.md` - Build scripts and development utilities
    - `CONFIGURATION.md` - Root-level configs and project setup
    - `ASPIRE_ORCHESTRATOR.md` - .NET Aspire orchestration and deployment

## Development Environment

**Quick Setup:**
- `make start` - Start all services (workbench service, frontend, and select assistants)
- `make stop` - Stop all services
- `make restart` - Restart all services

**Prerequisites:**
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- .NET 8.0+
- Make utility

**Environment Configuration:**
- Copy `.env.example` to `.env` and configure API keys
- Required: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Optional: `AZURE_OPENAI_*` keys for Azure OpenAI

## Architecture Overview

**Core Platform:**
- **Workbench Service** (FastAPI) - Central API and conversation management
- **Workbench Frontend** (React/TypeScript) - User interface
- **SQLite Database** - Conversation and state persistence

**Assistant Framework:**
- **Python Assistant Library** - Base classes and utilities for assistant development
- **MCP Integration** - Model Context Protocol for tool/resource access
- **Event System** - Pub/sub messaging between components

**Assistant Implementations:**
- **Project Assistant** - Multi-agent project management with file operations
- **Document Assistant** - Document processing and analysis
- **Codespace Assistant** - Development environment management
- **Navigator Assistant** - Workbench feature guidance
- **Prospector Assistant** - Advanced agent with artifact creation capabilities

## Common Development Tasks

**Running Individual Services:**
- `make workbench` - Start workbench service and frontend only
- `make assistant-<name>` - Start specific assistant (e.g., `make assistant-project`)
- `make mcp-server-<name>` - Start specific MCP server

**Testing:**
- `make test` - Run all tests
- `make test-python` - Run Python tests only
- `make test-frontend` - Run frontend tests only
- `make test-assistants` - Run assistant tests

**Development Tools:**
- `make format` - Format all code (Python, TypeScript, etc.)
- `make lint` - Run linters
- `make type-check` - Run type checking
- `make clean` - Clean build artifacts

**Database Management:**
- `make db-reset` - Reset database to clean state
- `make db-migrate` - Run database migrations
- `make db-seed` - Seed with sample data

## Assistant Development

**Creating New Assistants:**
1. Use `semantic-workbench-assistant` library as base
2. Implement required handlers: `on_conversation_created`, `on_user_message`
3. Register with workbench service via configuration
4. Add to `docker-compose.yml` for orchestration

**Key Patterns:**
- **State Management** - Use `ConversationContext` for persistent state
- **Tool Integration** - Implement MCP servers for external tool access
- **Event Handling** - Subscribe to conversation events for reactive behavior
- **Multi-Agent** - Use conversation participants for agent coordination

## Configuration Management

**Service Configuration:**
- Each service has `config.py` with Pydantic models
- Environment variables override defaults
- YAML configuration files for complex settings

**Assistant Configuration:**
- `assistant_config.json` defines capabilities and metadata
- Runtime configuration via workbench service API
- Per-conversation settings and preferences

## Deployment

**Local Development:**
- `make start` - Docker Compose orchestration
- Individual services can run outside Docker for debugging

**Production Deployment:**
- Use `docker-compose.prod.yml` for production
- Configure external database (PostgreSQL recommended)
- Set up reverse proxy for HTTPS termination
- Configure environment variables for all services

## Contributing

**Code Style:**
- Python: Black formatting, isort imports, flake8 linting
- TypeScript: Prettier formatting, ESLint rules
- Run `make format` before committing

**Pull Request Process:**
1. Create feature branch
2. Implement changes with tests
3. Run `make test` and `make lint`
4. Submit PR with description and testing notes

**Documentation:**
- Update `claude.md` for architectural changes
- Add docstrings for public APIs
- Update README files for new features