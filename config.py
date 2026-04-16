# Configuration settings
import os
import json
from dotenv import load_dotenv

load_dotenv()

# API Keys
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'job_results.xlsx')

# Load Actor IDs from JSON file (configurable via env variable)
ACTOR_IDS_FILE = os.getenv('ACTOR_IDS_FILE', 'actors.json')
try:
    with open(ACTOR_IDS_FILE, 'r') as f:
        ACTOR_IDS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Warning: Could not load ACTOR_IDS from {ACTOR_IDS_FILE}: {e}")
    ACTOR_IDS = {}

# Load Actor Run Inputs from JSON file (configurable via env variable)
ACTOR_RUN_INPUTS_FILE = os.getenv('ACTOR_RUN_INPUTS_FILE', 'actor_inputs.json')
try:
    with open(ACTOR_RUN_INPUTS_FILE, 'r') as f:
        ACTOR_RUN_INPUTS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Warning: Could not load ACTOR_RUN_INPUTS from {ACTOR_RUN_INPUTS_FILE}: {e}")
    ACTOR_RUN_INPUTS = {}

# Excel settings
EXCEL_SHEET_NAME = os.getenv('EXCEL_SHEET_NAME', 'Job Results')

# Ollama
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral:7b')

# File paths
FILTER_DOCUMENT_PATH = os.getenv('FILTER_DOCUMENT_PATH', 'filter_criteria.docx')
NORMALIZED_DATA_PATH = os.getenv('NORMALIZED_DATA_PATH', 'normalized_data.json')

# Webhook
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 5000))

# Apify sync endpoint timeout (max 300 seconds for synchronous endpoint)
APIFY_RUN_TIMEOUT = int(os.getenv('APIFY_RUN_TIMEOUT', 300))