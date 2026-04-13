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

```
├── main.py                              # Main entry point
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── src/
│   ├── apify_connector.py              # Apify API client
│   ├── webhook_listener.py             # Flask webhook server
│   ├── data_normalizer.py              # Data normalization
│   ├── llm_filter.py                   # Ollama LLM filtering
│   ├── excel_writer.py                 # Excel file writer
│   └── google_sheets_writer.py         # Google Sheets integration
├── README.md
├── NORMALIZATION_UPDATE.md             # Schema normalization summary
├── UNIFIED_SCHEMA.md                   # Complete field reference
├── SCHEMA_TRANSFORMATION_EXAMPLES.md   # Transformation examples
└── USAGE_GUIDE.md                      # Quick start guide
```

## Schema Normalization

This project normalizes job postings from 3 sources (Naukri, LinkedIn, Indeed) into a single unified schema with 50+ flat columns, perfect for Excel export.

### Key Improvements

- ✅ **Flat Structure**: All data in individual columns (not nested JSON)
- ✅ **Excel-Friendly**: Export directly to Excel without additional processing
- ✅ **Consistent Format**: Same schema across all sources
- ✅ **Easy Filtering**: Filter by company, location, salary, skills, etc.
- ✅ **Complete Data**: 50+ fields covering job, company, location, compensation, skills

### Documentation Files

| File                                                                   | Purpose                                  |
| ---------------------------------------------------------------------- | ---------------------------------------- |
| [UNIFIED_SCHEMA.md](UNIFIED_SCHEMA.md)                                 | Complete field reference and definitions |
| [SCHEMA_TRANSFORMATION_EXAMPLES.md](SCHEMA_TRANSFORMATION_EXAMPLES.md) | Real-world transformation examples       |
| [USAGE_GUIDE.md](USAGE_GUIDE.md)                                       | Quick start and common tasks             |
| [NORMALIZATION_UPDATE.md](NORMALIZATION_UPDATE.md)                     | Summary of changes from previous version |

### Quick Example

```python
from src.data_normalizer import DataNormalizer
from src.excel_writer import ExcelWriter

# Normalize job data from multiple sources
normalizer = DataNormalizer()
jobs = normalizer.normalize_actor_data([indeed_jobs, linkedin_jobs, naukri_jobs])

# Export to Excel with all 50+ columns
excel = ExcelWriter('job_listings.xlsx')
excel.write_data(jobs)

print(f"✅ Normalized {len(jobs)} jobs to Excel")
```

### Unified Schema Sample Columns

- **Basic Info**: job_id, job_title, job_url, source, posted_date, job_description
- **Company**: company_name, company_logo, company_website, company_rating, company_employees
- **Location**: job_location, job_city, job_country, job_latitude, job_longitude
- **Compensation**: salary_min, salary_max, salary_currency, salary_type
- **Experience**: min_experience_years, max_experience_years, experience_text
- **Skills**: required_skills, preferred_skills, all_skills
- **Details**: job_role, industry, employment_type, job_vacancies, benefits
- **...and 25+ more fields**

For complete field reference, see [UNIFIED_SCHEMA.md](UNIFIED_SCHEMA.md)</content>
<parameter name="filePath">c:\Shiv\Projects\AIML\JobAutoPipeline\README.md

```

```
