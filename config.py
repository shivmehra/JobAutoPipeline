# Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
APIFY_WEBHOOK_URL = os.getenv('APIFY_WEBHOOK_URL')
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'job_results.xlsx')

# Actor IDs (replace with actual actor IDs)
ACTOR_IDS = {
    'borderline/indeed-scraper': 'MXLpngmVpE8WTESQr',
    'curious_coder/linkedin-jobs-scraper': 'hKByXkMQaC5Qt9UMN',
    'memo23/naukri-scraper': 'EYXvM0o2lS7rYzgey'
}

# Excel settings
EXCEL_SHEET_NAME = os.getenv('EXCEL_SHEET_NAME', 'Job Results')

# Ollama
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral:7b')

# File paths
FILTER_DOCUMENT_PATH = os.getenv('FILTER_DOCUMENT_PATH', 'filter_criteria.docx')
NORMALIZED_DATA_PATH = os.getenv('NORMALIZED_DATA_PATH', 'normalized_data.json')

# Webhook
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 5000))