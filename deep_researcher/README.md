# Deep Researcher Crew

Welcome to the Deep Researcher Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your environment variables into the `.env` file:**

- `OPENAI_API_KEY` - Your OpenAI API key for GPT models
- `SERPER_API_KEY` - Your Serper API key for web searches
- `PUSHOVER_USER` - Your Pushover user key for push notifications
- `PUSHOVER_TOKEN` - Your Pushover application token
- `TURSO_DATABASE_URL` - Your Turso Cloud database URL
- `TURSO_AUTH_TOKEN` - Your Turso Cloud authentication token

**Customize your crew:**

- Modify `src/deep_researcher/config/agents.yaml` to define your agents
- Modify `src/deep_researcher/config/tasks.yaml` to define your tasks
- Modify `src/deep_researcher/crew.py` to add your own logic, tools and specific args
- Modify `src/deep_researcher/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the deep-researcher Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example will:
- Create two research reports:
  - `outputs/report_en.md` - English research report
  - `outputs/report_zh.md` - Chinese translation of the research report
- Save the research record to the Turso Cloud database (topic, English report, and Chinese report)
- Send both reports to your device via Pushover notifications

## Understanding Your Crew

The deep-researcher Crew is composed of multiple AI agents, each with unique roles, goals, and tools:

1. **Researcher** - Conducts in-depth research on the specified topic using web search tools
2. **Writer** - Transforms research into well-written English reports
3. **Translator** - Translates the English report into Chinese while maintaining technical accuracy
4. **Recorder** - Saves research records to the Turso Cloud SQLite database for historical tracking
5. **Notifier** - Sends both reports via Pushover push notifications

These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Database Storage

The Deep Researcher system includes a **TursoDatabaseTool** that automatically saves all completed research records to a Turso Cloud SQLite database. Each research record includes:

- Research topic
- Complete English research report
- Complete Chinese research report
- Timestamp of when the record was created

The database tool requires the following environment variables:
- `TURSO_DATABASE_URL` - Your Turso Cloud database URL
- `TURSO_AUTH_TOKEN` - Your Turso Cloud authentication token

To set up a Turso database:
1. Sign up for a free account at [Turso](https://turso.tech/)
2. Create a new database
3. Run the schema from `databases/deep_researcher_schema.sql` to create the `research_records` table
4. Get your database URL and auth token from the Turso dashboard
5. Add them to your `.env` file

All research records are automatically archived by the **Recorder** agent, providing a complete history of all research conducted by the system.

## Support

For support, questions, or feedback regarding the Deep Researcher Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
