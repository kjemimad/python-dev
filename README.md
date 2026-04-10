# python-dev

A structured Python learning journey — 11 real-world projects built with clean code, tests, and proper documentation.

Each project is built from implementation to deployment, following professional development standards.

## Projects

| # | Project | Stack | Status |
|---|---------|-------|--------|
| 01 | [CLI Tool](./projects/01-cli-tool) | Click, Typer, PyPI | 🔧 In progress |
| 02 | [Scraper](./projects/02-scraper) | BeautifulSoup, Playwright | ⏳ Planned |
| 03 | [REST API](./projects/03-api-rest) | FastAPI, PostgreSQL, Docker | ⏳ Planned |
| 04 | [Monitoring Bot](./projects/04-monitoring-bot) | psutil, Slack API | ⏳ Planned |
| 05 | [ML Pipeline](./projects/05-ml-pipeline) | scikit-learn, pandas, MLflow | ⏳ Planned |
| 06 | [Dashboard](./projects/06-dashboard) | Streamlit, Plotly | ⏳ Planned |
| 07 | [CI/CD Pipeline](./projects/07-cicd) | GitHub Actions, pytest | ⏳ Planned |
| 08 | [Chatbot](./projects/08-chatbot) | LangChain, API Anthropic | ⏳ Planned |
| 09 | [RAG](./projects/09-rag) | ChromaDB, sentence-transformers | ⏳ Planned |
| 10 | [Agent](./projects/10-agent) | LangChain Agents, async Python | ⏳ Planned |
| 11 | [Open Source Lib](./projects/11-opensource-lib) | PyPI, MkDocs | ⏳ Planned |
| 12 | [SaaS](./projects/12-saas) | FastAPI, Stripe, PostgreSQL | ⏳ Planned |

## Code Quality Standards

Every project in this repo follows the same standards :

- **Typed** — type hints on every function signature
- **Tested** — unit and integration tests with pytest
- **Documented** — clear README, docstrings on every public function
- **Linted** — ruff for linting, black for formatting
- **Containerized** — Docker when relevant
- **CI/CD** — GitHub Actions from project 07 onwards

## Structure

Each project follows the same internal structure :

    project-name/
    ├── src/                  # source code
    ├── tests/                # all tests
    ├── docs/                 # project documentation
    ├── .env.example          # environment variables template
    ├── Dockerfile            # when relevant
    ├── pyproject.toml        # dependencies and project config
    └── README.md             # project documentation

## Convention

Commits follow the Conventional Commits specification :

feat: add user authentication
fix: handle empty response from API
docs: update installation guide
test: add unit tests for parser
refactor: extract validation logic


## Author

[kjemimad](https://github.com/kjemimad)
