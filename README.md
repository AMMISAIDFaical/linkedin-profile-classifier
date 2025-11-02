# LinkedIn Profile Classifier

An end-to-end workspace for classifying LinkedIn profiles into business-relevant categories. The repository contains two complementary parts:

- A simple classification script that uses a LangChain agent and Bright Data to fetch profile details and classify each profile into predefined categories.
- (not finished yet) A LangGraph-based app (in `app/`) scaffolded for building richer agent workflows and running them locally via LangGraph Server/Studio.


## What you can do with this repo

- Classify LinkedIn profiles from a CSV and export results to a new CSV.
- Experiment with agent workflows (nodes/edges) using LangGraph.
- Extend the classification logic, data sources, and output schemas for production.


## Repository layout

```
.

├── app/
│   ├── src/├── agent.py # Example graph for LangGraph
│           └── data──├ Test Data.csv
│           └──retrivers├liprofile_scraper.py
│                       │third_party_bright_data.py  # Bright Data API client          
│   ├── tests/                      # Unit/integration tests for LangGraph app
│   └── pyproject.toml              # App packaging and dev deps
├── requirements.txt                # Root-level Python dependencies (script + dev)
├── Makefile                        # Template make targets (root)
├── .github/workflows/cicd.yml      # CI skeleton (uses the root Makefile)
├── Dockerfile                      # Placeholder (not used for running the app)
└── README.md                       # This file
```
git merge copilot/vscode1761835629820

## Prerequisites

- Python 3.10+
- A Bright Data API key (for profile scraping)
- Access to an LLM endpoint via GitHub Models (or update the code to use a different provider)
	- The script uses `ChatOpenAI` with `base_url=https://models.inference.ai.azure.com` and expects `GITHUB_TOKEN` for auth.
- Optional: LangSmith account for tracing (can be disabled).


## Quick start (classification script)

1) Create and activate a virtual environment and install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Configure environment variables. Copy the example file and fill in values.

```bash
cp .env.example .env
```

Required variables for the script in `src/agent.py`:

- `GITHUB_TOKEN`: token for GitHub Models inference endpoint.
- `BRIGHT_DATA_API_KEY`: key for Bright Data datasets API.
- Optional LangSmith variables if you want tracing: `LANGSMITH_TRACING`, `LANGSMITH_ENDPOINT`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`.

3) Prepare input data. By default the script reads `src/data/Test Data.csv` and expects at least:

- `LinkedIn URL`
- `First Name`

4) Run the classifier.

```bash
python src/agent.py
```

Output: a file named `Test Data - Classified.csv` at the repository root with a new "Profile Type" column.

Notes:

- The scraper currently sleeps ~40s per profile to accommodate Bright Data processing. Start with a small sample to validate.
- The script uses an absolute path for the input CSV inside the dev container. If running outside the dev container, adjust paths as needed in `src/agent.py`.


## LangGraph app (optional, for building richer agents)

The `app/` directory is a LangGraph template you can run locally with hot reload and LangGraph Studio.

```bash
cd app
pip install -e . "langgraph-cli[inmem]"
langgraph dev
```

Then open the Studio UI as prompted. The example graph is defined in `app/src/agent/graph.py`. Unit and integration tests live under `app/tests/`.


## Configuration

See `docs/CONFIGURATION.md` for a complete list and guidance. The most important variables are:

- `GITHUB_TOKEN` (required): auth for ChatOpenAI when `base_url` is set to GitHub Models.
- `GITHUB_MODEL` (optional): model name used by the agent. Falls back to a sensible default.
- `BRIGHT_DATA_API_KEY` (required): API key for Bright Data datasets.
- `LANGSMITH_*` (optional): enable tracing in development.

An example file is provided in `.env.example`. The repo's `.gitignore` already excludes `.env`.


## How it works

At a high level:

1. The agent receives a LinkedIn profile URL.
2. It calls the `get_profile_details_by_name` tool (a wrapper around Bright Data dataset API) once.
3. The LLM classifies the profile into one of the categories:
	 - Exited Entrepreneur
	 - Serial Business Angel
	 - Top Mentor
	 - Big Tech C-level
	 - Board Member / Private Investor
	 - Ex-Consulting
4. Results are written to a CSV.

The tool implementation is in `src/retrivers/third_party_bright_data.py`.


## Testing

There are two testing contexts:

- LangGraph app tests: run from the `app/` directory

	```bash
	cd app
	make test
	```

- Root-level tests (template): provided as placeholders and may not reflect the current code structure. Focus on the `app/` tests for actionable validation.


## CI/CD

The repo includes a basic GitHub Actions workflow at `.github/workflows/cicd.yml` that runs the targets in the root `Makefile`. You may want to adapt it to use the `app/` Makefile or update the root tests before enabling required checks.

If you use CI with external services (LLMs/Bright Data), configure repository/environment secrets in GitHub Actions and do not rely on `.env` files.


## Security and compliance

- Secrets management: Never commit real secrets to the repository. Use `.env` locally and GitHub Actions secrets in CI. If secrets were committed in the past, rotate them immediately.
- Data privacy and terms: Respect LinkedIn/Bright Data terms of service, applicable laws, and internal policies. Only process data you are authorized to process.
- Network and rate limits: Bright Data calls are synchronous and may be slow under load. Add retries/backoff and monitoring before production use.

See `docs/SECURITY.md` for detailed guidance.


## Troubleshooting

- Bright Data returns empty or slow responses: verify `BRIGHT_DATA_API_KEY`, dataset configuration, and allow sufficient processing time.
- LLM errors (401/403/429): ensure `GITHUB_TOKEN` is set and your account has access to GitHub Models. Consider setting `GITHUB_MODEL` to a permitted model.
- File path issues: adjust the CSV path in `src/agent.py` if you're not running inside the dev container.

See `docs/TROUBLESHOOTING.md` for more.


## Roadmap / Next steps

- Parameterize input/output paths and remove absolute paths.
- Replace blocking sleep with a polling mechanism or webhooks for Bright Data results.
- Add robust unit/integration tests at root level to replace placeholders.
- Add observability (LangSmith), structured logs, and retries around network calls.


## License

This project is licensed under the MIT License. See `LICENSE` for details.
