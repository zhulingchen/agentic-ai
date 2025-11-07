# Agentic AI

This repository contains AI agent projects powered by CrewAI.

## Projects

### Deep Researcher

A multi-agent AI system that conducts deep research on any topic, saves research records to a Turso Cloud SQLite database, and sends push notifications with the results.

See [deep_researcher/README.md](deep_researcher/README.md) for more details.

## GitHub Actions CI/CD Pipeline

This repository includes a GitHub Actions workflow that allows you to manually trigger research on any topic.

### Prerequisites

Before using the workflow, you need to configure the following secrets in your GitHub repository settings:

1. **OPENAI_API_KEY** - Your OpenAI API key for GPT models
2. **PUSHOVER_USER** - Your Pushover user key for push notifications
3. **PUSHOVER_TOKEN** - Your Pushover application token
4. **SERPER_API_KEY** - Your Serper API key for web searches
5. **TURSO_DATABASE_URL** - Your Turso Cloud database URL
6. **TURSO_AUTH_TOKEN** - Your Turso Cloud authentication token

To add secrets:
1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its corresponding value

### Running the Research Pipeline

1. Go to the **Actions** tab in your GitHub repository
2. Select **Deep Researcher** from the workflow list
3. Click **Run workflow**
4. Enter your research topic in the input field
5. Click **Run workflow** to start

The workflow will:
- Set up the Python environment
- Install all dependencies
- Run the Deep Researcher crew with your specified topic
- Generate research reports in both English and Chinese
- Save research records to the Turso Cloud database
- Send push notifications to your device with both reports
- Upload the research reports as artifacts (available for 30 days)

### Viewing Results

You can access the research results in two ways:

1. **Push Notifications**: You'll receive two push notifications on your device:
   - English version: Complete research report in English
   - Chinese version: Complete research report translated to Chinese
2. **GitHub Artifacts**: Download both research reports from the workflow run's artifacts section:
   - `report_en.md`: English research report
   - `report_zh.md`: Chinese research report

## Local Development

To run the Deep Researcher locally, see the instructions in [deep_researcher/README.md](deep_researcher/README.md).
