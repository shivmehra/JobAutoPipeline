# Job Auto Pipeline

A Python-based pipeline that:

1. Connects to Apify API to run web scraping actors
2. Listens for webhook notifications when actor runs complete
3. Normalizes data from multiple actors into a single JSON format
4. Filters items using local Ollama LLM based on criteria from a Word document
5. Saves filtered results to a local Excel file

## Setup

### Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Apify account with API token

### Installation

1. Clone or download this repository
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and configuration

5. Install and start Ollama:

   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull mistral:7b
   ```

6. Create your filter criteria Word document (`filter_criteria.docx`)

## Configuration

Edit the `config.py` file to set:

- Actor IDs for your Apify actors
- Excel file path and sheet name
- File paths
- Model names

## Usage

Run the main pipeline:

```bash
python main.py
```

The pipeline will:

1. Start a webhook listener
2. Run the configured Apify actors
3. Wait for webhook notifications
4. Process and normalize the data
5. Filter using LLM
6. Save results to a local Excel file

## Project Structure

````
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── src/
│   ├── apify_connector.py     # Apify API client
│   ├── webhook_listener.py    # Flask webhook server
│   ├── data_normalizer.py     # Data normalization
│   ├── llm_filter.py         # Ollama LLM filtering
│   └── google_sheets_writer.py # Google Sheets integration
└── README.md
```</content>
<parameter name="filePath">c:\Shiv\Projects\AIML\JobAutoPipeline\README.md
````
