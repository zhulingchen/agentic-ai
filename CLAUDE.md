# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI agent repository powered by CrewAI. The repository supports multiple CrewAI projects, each placed in its own directory at the root level. All projects share a common `tools/` package containing reusable tools.

The main project is **Deep Researcher**, a multi-agent system that conducts in-depth research on any topic, generates bilingual reports (English and Chinese), saves research records (including bilingual reports, research sources, and tags) to a Turso Cloud SQLite database, and pushes paginated bilingual reports via Pushover.

New CrewAI projects can be created at the root level (e.g., `new_project/`) and can leverage the shared tools by including `shared_tools` as a path dependency in their `pyproject.toml`.

## Documentation

This repository maintains multiple documentation files for different audiences:

- `CLAUDE.md` (this file) - Technical guidance for Claude Code when working with the codebase
- `README.md` - User-facing documentation covering repository overview and GitHub Actions workflow usage
- `deep_researcher/README.md` - End-user installation and usage guide for the **Deep Researcher** project

When making changes to project structure, setup steps, or functionality, ensure both technical and user-facing documentation remain synchronized.

## Development Setup

### Prerequisites
- Python >=3.10 <3.14
- UV package manager for dependency management

### Initial Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify uv version
uv --version

# Navigate to the deep_researcher directory
cd deep_researcher

# Install dependencies
uv sync

# Verify python version
uv run python --version
# Expected output: Python 3.10.x, 3.11.x, 3.12.x, or 3.13.x
```

### Environment Configuration
Create a `.env` file in `deep_researcher/` with the following variables:
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `SERPER_API_KEY` - Serper API key for web searches
- `PUSHOVER_USER` - Pushover user key for push notifications
- `PUSHOVER_TOKEN` - Pushover application token
- `TURSO_DATABASE_URL` - Turso Cloud database URL
- `TURSO_AUTH_TOKEN` - Turso Cloud authentication token

## Common Development Commands

### Running the Deep Researcher
```bash
# From the root directory
cd deep_researcher
crewai run

# With command-line arguments
crewai run --topic "Your research topic here"

# Or using the environment variable `CREW_TOPIC`
CREW_TOPIC="Your research topic here" crewai run
```

### Database Setup

The database schema is located at `databases/deep_researcher_schema.sql`. It defines three tables:
- `research_records` - Stores research topics and bilingual reports
- `research_sources` - Tracks URLs and sources used during research
- `research_tags` - Stores categorical tags for research records

#### Installing Turso CLI

```bash
# Install turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Verify installation
turso --version
```

#### Setting Up Your Turso Database

```bash
# Authenticate with Turso (opens browser for login)
turso auth login

# Create a new database
turso db create deep-research

# List all databases
turso db list

# View database details
turso db show deep-research

# Get the database URL (save this as TURSO_DATABASE_URL in .env)
turso db show deep-research --url
# Example output: libsql://deep-research-[org-name].turso.io

# Create an authentication token (save this as TURSO_AUTH_TOKEN in .env)
turso db tokens create deep-research
# Example output: {encoded header}.{encoded payload}.{encoded signature}

# Apply the database schema
turso db shell deep-research < databases/deep_researcher_schema.sql

# Verify tables were created
turso db shell deep-research "SELECT name FROM sqlite_master WHERE type='table';"
# Expected output:
# research_records
# research_sources
# research_tags

# Query the database directly
turso db shell deep-research "SELECT * FROM research_records LIMIT 5;"
```

#### Alternative: Apply Schema Interactively

```bash
# Open interactive shell
turso db shell deep-research

# Then paste the schema from databases/deep_researcher_schema.sql
# Or run each CREATE TABLE statement individually

# Verify tables
.tables
# Expected output:
# research_records
# research_sources
# research_tags

# Exit shell
.quit
```

## Architecture

### Project Structure
```
agentic-ai/
├── .github/
│   └── workflows/
│       └── deep-researcher.yml   # GitHub Actions workflow
├── .gitignore                    # Git ignore patterns
├── CLAUDE.md                     # This file - technical guidance for Claude Code
├── README.md                     # User-facing repository documentation
├── deep_researcher/              # Main CrewAI project
│   ├── .env                      # Environment variables (not in git)
│   ├── .venv/                    # Virtual environment (not in git)
│   ├── README.md                 # End-user installation and usage guide
│   ├── pyproject.toml            # Dependencies and project metadata
│   ├── uv.lock                   # UV lock file
│   ├── src/deep_researcher/
│   │   ├── crew.py               # Agent and task definitions
│   │   ├── main.py               # Entry point
│   │   ├── schema.py             # Pydantic models for structured outputs
│   │   └── config/
│   │       ├── agents.yaml       # Agent roles, goals, and backstories
│   │       └── tasks.yaml        # Task descriptions and expected outputs
│   ├── outputs/                  # Generated research reports (not in git)
│   └── knowledge/                # Knowledge base for RAG (optional)
├── tools/                        # Shared tools package
│   └── src/shared_tools/
│       ├── turso_base_tool.py              # Base class for Turso tools
│       ├── turso_research_record_tool.py   # Save research records
│       ├── turso_research_sources_tool.py  # Save research sources
│       └── pushover_tool.py                # Send push notifications
└── databases/
    └── deep_researcher_schema.sql  # Database schema
```

### Multi-Agent System

The Deep Researcher uses 5 specialized agents working sequentially:

1. **Researcher** (gpt-4o) - Conducts investigative research using SerperDevTool
   - Limited to maximum 4 internet searches
   - Returns structured `ResearchOutput` with sources, tags, and metadata
   - Focuses on one specific subtopic with depth over breadth

2. **Writer** (gpt-4o) - Transforms research into publication-quality English reports
   - Creates 1200-1800 word reports in paragraph format (no bullet points except in Key Takeaways/Sources)
   - Saves to `outputs/report_en.md`

3. **Translator** (gpt-4o) - Translates English reports to Chinese
   - Maintains complete fidelity to source content
   - Preserves all URLs and citations in original English
   - Saves to `outputs/report_zh.md`

4. **Recorder** (gpt-4o-mini) - Archives research to Turso database
   - Saves research record using `TursoResearchRecordTool`
   - Saves all sources using `TursoResearchSourcesTool`

5. **Notifier** (gpt-4o-mini) - Sends push notifications
   - Sends two notifications (English and Chinese) via Pushover
   - Includes full report content in markdown format

### Shared Tools Package

The `tools/` directory contains a separate Python package (`shared_tools`) with reusable CrewAI tools:

- **TursoBaseTool**: Abstract base class that handles Turso database connections using `libsql`
  - Connection credentials from `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` environment variables
  - All Turso tools inherit from this base class

- **TursoResearchRecordTool**: Saves research records to the `research_records` table
  - Returns `research_id` for linking sources

- **TursoResearchSourcesTool**: Saves research sources to the `research_sources` table
  - Links sources to research records via `research_id`

- **PushoverNotificationTool**: Sends push notifications via Pushover API
  - Accepts title and message parameters

The `deep_researcher` project includes `shared_tools` as an editable dependency via UV's path source configuration.

### Task Dependencies and Context

Tasks use CrewAI's context mechanism to pass outputs between agents:
- `writing_task` receives context from `research_task`
- `translation_task` receives context from `writing_task`
- `recording_task` receives context from all three previous tasks
- `notification_task` receives context from `writing_task` and `translation_task`

### Pydantic Schemas

The `schema.py` file defines structured outputs for the research task:
- `ResearchSource` - Individual source metadata with URL, title, relevance, quality score
- `ResearchOutput` - Complete research output with sources, summary, tags, confidence level, and limitations
- Enums: `ResearchDepth` (surface/moderate/comprehensive) and `ConfidenceLevel` (low/medium/high)

## Important Constraints

### Research Task Limits
- Maximum 4 internet searches per research run (critical constraint)
- Must focus on one specific subtopic with depth over breadth
- Must include at least 5 distinct sources
- Must provide 3-7 categorical tags

### Writing Requirements
- 1200-1800 word reports in paragraph format
- NO bullet points in main sections (only in Key Takeaways and Sources)
- Each main section must contain 3-6 full paragraphs (4-8 sentences each)
- Minimum 5 concrete examples with specific details
- All claims must be cited with source URLs

### Translation Requirements
- Complete fidelity to source content (no additions/deletions/hallucinations)
- Keep all URLs, citations, author names, and publication names in original English
- Translate only narrative text, not references

## GitHub Actions CI/CD

The repository includes a workflow at `.github/workflows/deep-researcher.yml`:
- Manually triggered via workflow_dispatch with a topic input
- Sets up Python 3.12 and UV
- Runs research and uploads reports as artifacts
- Requires all 6 secrets configured in GitHub repository settings

## Key Design Patterns

1. **Agent Specialization**: Each agent has a single, well-defined responsibility with appropriate LLM model selection (gpt-4o for creative tasks, gpt-4o-mini for utility tasks)

2. **Sequential Processing**: Uses `Process.sequential` to ensure tasks complete in dependency order

3. **Structured Outputs**: Research task uses Pydantic models (`output_pydantic=ResearchOutput`) to ensure consistent, parseable results

4. **Shared Tooling**: Common database and notification functionality extracted into reusable tools package

5. **Configuration Separation**: Agent behaviors and task definitions stored in YAML files for easy modification without code changes
