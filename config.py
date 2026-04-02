# Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')

# Actor IDs (replace with actual actor IDs)
ACTOR_IDS = {
    'actor1': 'your-actor-id-1',
    'actor2': 'your-actor-id-2',
    'actor3': 'your-actor-id-3'
}

# Google Sheets
SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Job Pipeline Results')

# Ollama
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral:7b')

# File paths
FILTER_DOCUMENT_PATH = os.getenv('FILTER_DOCUMENT_PATH', 'filter_criteria.docx')
NORMALIZED_DATA_PATH = os.getenv('NORMALIZED_DATA_PATH', 'normalized_data.json')

# Webhook
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 5000))</content>
<parameter name="filePath">c:\Shiv\Projects\AIML\JobAutoPipeline\config.py