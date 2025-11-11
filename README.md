# Cardano Summit Hack - URL to Markdown Agent

A CrewAI-powered agent that transforms web page content into well-formatted Markdown using Google's Gemini API.

## Features

- Fetches content from any URL
- Uses CrewAI with multiple specialized agents:
  - **Web Content Analyzer**: Extracts and analyzes key information
  - **Markdown Formatter**: Transforms content into clean markdown
- Powered by Google Gemini 2.5 Flash model
- Saves output to a markdown file

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/semsorock/cardano-summit-hack.git
   cd cardano-summit-hack
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```
   - Get your API key from: https://makersuite.google.com/app/apikey

## Usage

### Test the Installation

Before running the agent, you can verify the installation:
```bash
python test_structure.py
```

This will validate that all components are properly installed and configured.

### Run the Agent

Run the agent with the default example URL:
```bash
python url_to_markdown_agent.py
```

The agent will:
1. Fetch content from the URL (default: Catalyst Explorer proposal page)
2. Analyze the content to extract key information
3. Transform it into well-formatted markdown
4. Save the output to `output.md`

### Customize the URL

Edit the `main()` function in `url_to_markdown_agent.py` to change the target URL:
```python
def main():
    url = "https://your-target-url.com"
    # ... rest of the code
```

## Example

Default example transforms this URL:
```
https://www.catalystexplorer.com/en/proposals/cardano-india-developers-community-hub-f14/details
```

Into a structured markdown document with:
- Title and headers
- Project description
- Budget information
- Key details and dates
- Properly formatted lists and sections

## Requirements

- Python 3.8+
- Google Gemini API key
- Internet connection for fetching URLs

## Dependencies

- `crewai`: Multi-agent framework
- `google-generativeai`: Google Gemini API client
- `requests`: HTTP library for fetching URLs
- `beautifulsoup4`: HTML parsing
- `python-dotenv`: Environment variable management

## License

MIT