# LinkedIn Profile Classifier

[![CI](https://github.com/AMMISAIDFaical/linkedin-profile-classifier/actions/workflows/cicd.yml/badge.svg)](https://github.com/AMMISAIDFaical/linkedin-profile-classifier/actions/workflows/cicd.yml)

An intelligent AI agent that classifies LinkedIn profiles into various professional categories using LangGraph and OpenAI's GPT models. This tool helps identify and categorize professionals based on their LinkedIn profile data.

## 📋 Overview

This project uses LangChain and LangGraph to create an AI agent that:
- Scrapes LinkedIn profile data using Bright Data API
- Analyzes professional backgrounds and experience
- Classifies profiles into predefined categories
- Generates structured output with reasoning

### Profile Categories

The classifier identifies the following profile types:
- **Exited Entrepreneur**: Founders who have successfully exited their companies
- **Serial Business Angel**: Individual investors in startups (not via funds)
- **Top Mentor**: Professionals who mentor founders or startups
- **Big Tech C-level**: Executives (CEO, CTO, CIO, VP, Director) at major tech companies
- **Board Member / Private Investor**: Board members or private equity/VC investors
- **Ex-Consulting**: Former consultants from top consulting firms

## 🚀 Features

- **Automated Profile Classification**: Classify LinkedIn profiles with AI-powered analysis
- **Batch Processing**: Process multiple profiles from CSV files
- **LangGraph Integration**: Visual debugging and workflow orchestration
- **Structured Output**: Get classification results with detailed reasoning
- **LangSmith Tracing**: Monitor and debug AI agent behavior

## 📁 Project Structure

```
linkedin-profile-classifier/
├── app/                      # LangGraph application
│   ├── src/agent/           # Agent graph implementation
│   ├── retrivers/           # LinkedIn data retrieval modules
│   └── tests/               # Unit and integration tests
├── src/                     # Source code
│   ├── agent.py            # Main classification agent
│   ├── retrivers/          # LinkedIn scraping utilities
│   └── data/               # Test data files
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
└── Makefile               # Build and test commands
```

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Bright Data API key (for LinkedIn scraping)
- OpenAI API key or GitHub Models API access

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AMMISAIDFaical/linkedin-profile-classifier.git
cd linkedin-profile-classifier
```

2. Install dependencies:
```bash
make install
# or
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp app/.env.example .env
```

Edit `.env` and add your API keys:
```env
GITHUB_TOKEN=your_github_token_here
BRIGHT_DATA_API_KEY=your_bright_data_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_project_name
```

## 📖 Usage

### Basic Usage

Run the classification agent on test data:

```bash
python src/agent.py
```

This will:
1. Load profiles from `src/data/Test Data.csv`
2. Fetch LinkedIn profile details via Bright Data API
3. Classify each profile using GPT-4
4. Save results to `Test Data - Classified.csv`

### CLI Usage

Use the command-line interface:

```bash
python main.py add 5 10
```

### Using LangGraph Server

For development with visual debugging:

1. Navigate to the app directory:
```bash
cd app
```

2. Install LangGraph CLI:
```bash
pip install -e . "langgraph-cli[inmem]"
```

3. Start the LangGraph development server:
```bash
langgraph dev
```

4. Open LangGraph Studio to visualize and debug your agent workflows.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
make test

# Run unit tests only
cd app && make test

# Run integration tests
cd app && make integration_tests

# Run tests with coverage
python -m pytest -vv --cov=main --cov=mylib test_*.py
```

## 🔧 Development

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
make format

# Lint code
make lint

# Run full quality check
make refactor
```

### Project Structure

- **`src/agent.py`**: Main classification logic for batch processing
- **`app/src/agent/graph.py`**: LangGraph agent implementation
- **`src/retrivers/`**: LinkedIn profile scraping modules
- **`main.py`**: Command-line interface

## 🐳 Docker

Build and run with Docker:

```bash
docker build -t linkedin-classifier .
docker run linkedin-classifier
```

## 📊 Data Format

### Input CSV Format

```csv
First Name,Profile Type,LinkedIn URL
John,,"https://linkedin.com/in/johndoe"
Jane,,"https://linkedin.com/in/janedoe"
```

### Output CSV Format

```csv
First Name,Profile Type,LinkedIn URL,profile type
John,"Exited Entrepreneur","https://linkedin.com/in/johndoe","Exited Entrepreneur"
Jane,"Board Member / Private Investor","https://linkedin.com/in/janedoe","Board Member / Private Investor"
```

## 🔑 API Keys & Configuration

This project requires:

1. **GitHub Token** or **OpenAI API Key**: For GPT model access
2. **Bright Data API Key**: For LinkedIn profile scraping
3. **LangSmith API Key** (Optional): For tracing and debugging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based agent orchestration
- [Bright Data](https://brightdata.com/) - LinkedIn profile data collection
- OpenAI - GPT models for classification

## 📞 Support

For questions or issues, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Add support for more profile categories
- [ ] Implement caching for API responses
- [ ] Add web interface for profile classification
- [ ] Support for bulk processing with progress tracking
- [ ] Enhanced error handling and retry logic
- [ ] Add more comprehensive test coverage
