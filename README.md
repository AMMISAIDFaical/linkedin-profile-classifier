# LinkedIn Profile Classifier

An AI-powered tool that classifies LinkedIn profiles into VC firm-relevant categories using LangChain agents and OpenAI models. The system intelligently retrieves profile data and categorizes professionals based on their career history and expertise.

## Overview

This project uses AI agents to automatically classify LinkedIn profiles into specific categories relevant to venture capital firms and innovation ecosystems. It leverages LangChain, LangGraph, and OpenAI models to analyze profile data and make intelligent classification decisions.

**Classification Categories:**
- **Exited Entrepreneur**: Founded a company
- **Serial Business Angel**: Invests in startups personally (not via fund)
- **Top Mentor**: Mentors founders or startups
- **Big Tech C-level**: Executive (CEO, CTO, CIO, VP, Director)
- **Board Member / Private Investor**: Serves on company boards or invests via private equity/venture capital
- **Ex-Consulting**: Formerly worked at top consulting firms

## Features

- 🤖 **AI Agent-Based Classification**: Uses LangChain agents with structured output for consistent results
- 🔍 **Multiple Data Retrieval Methods**: Supports both third-party APIs (Bright Data) and custom scrapers
- 📊 **CSV Batch Processing**: Process multiple profiles from CSV files
- 🔐 **Secure Configuration**: Environment-based configuration for API keys and credentials
- 🎯 **Structured Output**: Pydantic models ensure type-safe classification results

## Quick Start

### Prerequisites

- Python 3.8+
- GitHub token with access to Azure OpenAI models
- Bright Data API key (for profile data retrieval)
- LinkedIn credentials (if using custom scraper)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AMMISAIDFaical/linkedin-profile-classifier.git
   cd linkedin-profile-classifier
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_token_here
   GITHUB_MODEL=gpt-4o-mini
   BRIGHT_DATA_API_KEY=your_bright_data_api_key
   LINKEDIN_EMAIL=your_linkedin_email
   LINKEDIN_PASSWORD=your_linkedin_password
   ```

### Usage

#### Basic Classification

Run the agent to classify profiles from a CSV file:

```bash
python src/agent.py
```

The script will:
1. Read LinkedIn URLs from your input CSV
2. Retrieve profile details using Bright Data API
3. Classify each profile using the AI agent
4. Save results to `Test Data - Classified.csv`

#### Using Custom Scraper

For more control over data retrieval:

```bash
python src/retrivers/liprofile_scraper.py
```

This uses Selenium to scrape profiles directly (requires LinkedIn credentials).

#### Simple CLI Tool

```bash
python main.py add 5 3
```

## Project Structure

```
linkedin-profile-classifier/
├── src/
│   ├── agent.py                    # Main classification agent
│   ├── retrivers/
│   │   ├── third_party_bright_data.py  # Bright Data API integration
│   │   └── liprofile_scraper.py        # Selenium-based scraper
│   └── data/                       # Data files
├── app/
│   ├── src/agent/
│   │   └── graph.py               # LangGraph implementation
│   ├── retrivers/                 # App-level retrievers
│   └── tests/                     # Unit and integration tests
├── main.py                        # CLI entry point
├── test_main.py                   # Basic tests
├── requirements.txt               # Python dependencies
├── Makefile                       # Common tasks
├── Dockerfile                     # Container configuration
└── README.md                      # This file
```

## Configuration

### AI Model Configuration

The agent uses Azure OpenAI models via GitHub's inference API. Configure in your `.env`:

```env
GITHUB_MODEL=gpt-4o-mini  # or gpt-5, gpt-4, etc.
```

### Profile Retrieval Options

**Option 1: Bright Data API (Recommended)**
- Set `BRIGHT_DATA_API_KEY` in `.env`
- Handles rate limiting automatically (40s delay between requests)
- More reliable and respectful of LinkedIn's terms

**Option 2: Custom Scraper**
- Set `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` in `.env`
- Uses Selenium with Chrome WebDriver
- Supports headless mode

## Development

### Running Tests

```bash
make test
```

Or directly with pytest:
```bash
python -m pytest -vv --cov=main --cov=src test_*.py
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Both format and lint
make refactor
```

### CI/CD

The project includes GitHub Actions workflows for continuous integration:
- `.github/workflows/cicd.yml`: Main CI pipeline
- `app/.github/workflows/unit-tests.yml`: Unit tests
- `app/.github/workflows/integration-tests.yml`: Integration tests

## Data Format

### Input CSV Format

Your input CSV should have at minimum:
- `LinkedIn URL`: Full LinkedIn profile URL
- `First Name`: Person's first name (for logging)

Example:
```csv
First Name,Last Name,LinkedIn URL
John,Doe,https://linkedin.com/in/johndoe
Jane,Smith,https://linkedin.com/in/janesmith
```

### Output Format

The classified CSV will include all original columns plus:
- `Profile Type`: The assigned classification category

## Advanced Usage

### Customizing Classification Categories

Edit the `ProfileType` model in `src/agent.py`:

```python
class ProfileType(BaseModel):
    profile_type: Literal[
        "Your Category 1",
        "Your Category 2",
        # Add more categories
    ] = Field(description="The profile type of the person")
```

### Adjusting the Agent Prompt

Modify the classification logic by editing the `prompt` variable in `src/agent.py`:

```python
prompt = """Your custom instructions here..."""
```

### Using Different Models

Change the model in `src/agent.py`:

```python
model = ChatOpenAI(
    model="gpt-4",  # or other available models
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)
```

## Docker Deployment

Build the Docker image:
```bash
docker build -t linkedin-profile-classifier .
```

Run the container:
```bash
docker run -d \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  linkedin-profile-classifier
```

## Make Commands

The `Makefile` provides convenient shortcuts:

- `make install`: Install all dependencies
- `make test`: Run tests with coverage
- `make format`: Format code with Black
- `make lint`: Lint code with Pylint
- `make refactor`: Format and lint
- `make all`: Install, lint, test, format, and deploy

## Security and Privacy

⚠️ **Important Considerations:**

1. **API Keys**: Never commit `.env` files or expose API keys
2. **LinkedIn Terms**: Ensure compliance with LinkedIn's Terms of Service
3. **Data Privacy**: Handle personal information responsibly
4. **Rate Limiting**: Respect API rate limits (currently 40s delay between requests)
5. **PII Protection**: Remove unnecessary personal identifiable information

## Troubleshooting

### Common Issues

**Issue**: `No module named 'langchain'`
```bash
pip install -r requirements.txt
```

**Issue**: Bright Data API timeout
- Check your API key is valid
- Ensure you have sufficient credits
- Increase the sleep delay in `third_party_bright_data.py`

**Issue**: Selenium WebDriver not found
```bash
# Install Chrome WebDriver
pip install webdriver-manager
```

**Issue**: GitHub model authentication failure
- Verify your `GITHUB_TOKEN` has appropriate permissions
- Check token hasn't expired

## Roadmap

- [ ] Support for multi-label classification
- [ ] Web UI for profile uploads and review
- [ ] Integration with more profile data sources
- [ ] Real-time classification API endpoint
- [ ] Enhanced caching and rate limit handling
- [ ] Support for batch async processing
- [ ] Model fine-tuning on domain-specific data

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Run `make refactor` before committing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) Microsoft Corporation.

## Acknowledgments

- **LangChain**: Framework for building AI agents
- **LangGraph**: Graph-based agent orchestration
- **OpenAI**: Language models via Azure
- **Bright Data**: Profile data retrieval
- **Selenium**: Web automation
- **FastAPI & Uvicorn**: API framework (future integration)
- **Pandas**: Data manipulation
- **Pydantic**: Data validation

## Support

For issues, questions, or contributions:
- 🐛 [Report bugs](https://github.com/AMMISAIDFaical/linkedin-profile-classifier/issues)
- 💡 [Request features](https://github.com/AMMISAIDFaical/linkedin-profile-classifier/issues)
- 📧 Contact the maintainer

---

**Disclaimer**: This tool is designed for legitimate use cases such as investor network analysis, talent mapping, and professional categorization. Always ensure compliance with LinkedIn's Terms of Service and applicable data protection regulations.