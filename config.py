# Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'job_results.xlsx')

# Actor IDs (replace with actual actor IDs)
ACTOR_IDS = {
    'borderline/indeed-scraper': 'MXLpngmVpE8WTESQr',
    'curious_coder/linkedin-jobs-scraper': 'hKByXkMQaC5Qt9UMN',
    'memo23/naukri-scraper': 'EYXvM0o2lS7rYzgey'
}

# Per-actor input payloads. Customize the keys and values to match each actor's expected run input.
ACTOR_RUN_INPUTS = {
    'borderline/indeed-scraper': {
        "country": "in",
        "enableUniqueJobs": True,
        "fromDays": "1",
        "includeSimilarJobs": False,
        "jobType": "fulltime",
        "level": "entry_level",
        "location": "Mumbai, Maharashtra",
        "maxRows": 5,
        "maxRowsPerUrl": 3,
        "query": "Analyst",
        "remote": "hybrid",
        "sort": "relevance",
        "urls": [
            "https://in.indeed.com/jobs?q=ai+developer&l=Mumbai%2C+Maharashtra&fromage=3&radius=25&sc=0kf%3Aattr%28CF3CP%29%3B&from=searchOnDesktopSerp&vjk=081ff9624c1074d7",
            "https://in.indeed.com/jobs?q=front+end+developer&l=Mumbai%2C+Maharashtra&fromage=3&radius=25&sc=0kf%3Aattr%285QWDV%7C7EQCZ%7CCF3CP%252COR%29attr%286M28R%7C84K74%7CFGY89%7CJB2WC%7CNGEEK%7CX62BT%7CY7U37%252COR%29%3B&from=searchOnDesktopSerp&vjk=eba79aef448b8e17"
        ]
    },
    'curious_coder/linkedin-jobs-scraper': {
    "count": 10,
    "scrapeCompany": True,
    "splitByLocation": False,
    "splitCountry": "IN",
    "urls": [
        "https://in.linkedin.com/jobs/search?keywords=AI%20Developer&location=India&geoId=102713980&f_JT=F&f_PP=105214831%2C105556991%2C103671728%2C106164952&f_TPR=r86400&position=1&pageNum=0"
    ]
},
    'memo23/naukri-scraper': {
        "includeAmbitionBoxDetails": False,
        "maxConcurrency": 1,
        "maxRequestRetries": 2,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": [
                "RESIDENTIAL"
            ],
            "apifyProxyCountry": "IN"
        },
        "startUrls": [
            "https://www.naukri.com/ai-developer-jobs-in-mumbai-all-areas?k=ai%20developer&l=mumbai%20(all%20areas)%2C%20pune%2C%20hyderabad%2C%20bengaluru&nignbevent_src=jobsearchDeskGNB&experience=0&jobAge=1"
        ]
    }
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

# Apify sync endpoint timeout (max 300 seconds for synchronous endpoint)
APIFY_RUN_TIMEOUT = int(os.getenv('APIFY_RUN_TIMEOUT', 300))