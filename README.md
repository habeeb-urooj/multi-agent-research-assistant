# Multi-Agent Research Assistant

An AI-powered research assistant that uses multiple specialized agents to plan, research, fact-check, and synthesize information into a structured final report.

The system breaks a complex research question into multiple tasks, executes research branches in parallel, validates the findings through critic agents, and combines the validated results into a final response.

## Architecture

```text
                    User Query
                        │
                        ▼
                  ┌───────────┐
                  │  Planner  │
                  └─────┬─────┘
                        │
              Research Tasks
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 ┌────────────┐  ┌────────────┐  ┌────────────┐
 │ Researcher │  │ Researcher │  │ Researcher │
 │     1      │  │     2      │  │     3      │
 └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
       │               │               │
       ▼               ▼               ▼
 ┌────────────┐  ┌────────────┐  ┌────────────┐
 │  Critic 1  │  │  Critic 2  │  │  Critic 3  │
 └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                ┌──────────────┐
                │ Synthesizer  │
                └──────┬───────┘
                       │
                       ▼
                 Final Report
```

## Key Features

* Multi-agent research pipeline for complex questions
* Automated research planning using an LLM
* Parallel research execution to reduce pipeline latency
* SearXNG integration for web search
* Independent critic agents for validating research findings
* LLM-based synthesis of validated results
* FastAPI REST API for programmatic access
* Docker-based SearXNG setup
* Configurable model and API settings through environment variables
* Logging and execution-time tracking

## Tech Stack

* Python
* FastAPI
* OpenRouter API
* SearXNG
* Docker
* Pydantic
* Requests
* Concurrent execution with ThreadPoolExecutor
* Git & GitHub

## Project Structure

```text
multi-agent-research-assistant/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── critic.py
│   │   └── synthesizer.py
│   │
│   ├── config/
│   │   ├── limits.py
│   │   └── settings.py
│   │
│   ├── pipeline/
│   │   └── research_pipeline.py
│   │
│   ├── tools/
│   │   └── web_search.py
│   │
│   └── main.py
│
├── searxng/
│   └── settings.yml
│
├── docker-compose.yml
├── requirements.txt
├── test_pipeline.py
├── test_researcher.py
├── test_critic.py
├── .gitignore
└── README.md
```

## How It Works

### 1. Planner

The planner receives the user's research question and breaks it into multiple focused research tasks.

### 2. Researchers

Each research task is assigned to a separate researcher branch.

Researchers use SearXNG to retrieve relevant web search results and an LLM to analyze the collected information.

The research branches execute concurrently rather than sequentially.

### 3. Critics

Each research branch is passed to a critic agent.

The critic evaluates the research findings and produces a validation verdict before the information reaches the synthesis stage.

### 4. Synthesizer

The synthesizer combines the validated findings from all research branches and generates a final research report.

## Example Research Query

```text
How are multi-agent AI systems being used to automate software development?
```

The planner may divide this into tasks such as:

1. Current architectures and frameworks
2. SDLC use cases
3. Performance, efficiency, and limitations

The research branches are then executed concurrently, reviewed by critics, and combined into a final report.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/habeeb-urooj/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

### 5. Start SearXNG

```bash
docker compose up -d
```

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API

The main research endpoint is:

```text
POST /research
```

Example request:

```json
{
  "query": "How are multi-agent AI systems being used in software development?"
}
```

The API runs the complete research pipeline and returns the generated research output.

## Testing

Individual components can be tested using:

```bash
python test_researcher.py
```

```bash
python test_critic.py
```

```bash
python test_pipeline.py
```

## Environment Variables

| Variable             | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| `OPENROUTER_API_KEY` | API key used to access the selected LLM through OpenRouter |

Additional model and pipeline configuration is maintained within the application's configuration modules.

## Design Goals

This project demonstrates how multiple specialized AI agents can collaborate on a complex task instead of relying on a single LLM call.

The architecture focuses on:

* Task decomposition
* Parallel execution
* Independent validation
* Information synthesis
* Tool-augmented research
* API-based access

## Future Improvements

* Persistent research history
* Source citation tracking
* Improved source quality ranking
* Streaming research results
* User authentication
* Frontend interface
* Additional search providers
* Production deployment
* More sophisticated agent coordination

## Author

**Habeeb Urooj**

AI / ML Engineer

GitHub: https://github.com/habeeb-urooj
