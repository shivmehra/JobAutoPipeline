# Usage Guide: Normalized Job Schema

This guide shows how to use the updated `DataNormalizer` to convert job postings from multiple sources into a unified, Excel-friendly format.

## Quick Start

### Basic Usage

```python
from src.data_normalizer import DataNormalizer
import json

# Initialize normalizer
normalizer = DataNormalizer()

# Load raw data from APIs/scrapers
with open('raw_job_data.json', 'r') as f:
    raw_data = json.load(f)

# actor_data_list should be a list of datasets from different sources
# Structure: [indeed_jobs_list, linkedin_jobs_list, naukri_jobs_list]
actor_data_list = [raw_data]

# Normalize the data
normalized_jobs = normalizer.normalize_actor_data(actor_data_list)

# Save to JSON
normalizer.save_to_json('normalized_data.json')

print(f"Normalized {len(normalized_jobs)} jobs")
```

### Export to Excel

```python
from src.excel_writer import ExcelWriter
from src.data_normalizer import DataNormalizer

# Load normalized data
normalizer = DataNormalizer()
normalizer.load_from_json('normalized_data.json')

# Create Excel writer
excel_writer = ExcelWriter('job_listings.xlsx')

# Write normalized data to Excel
excel_writer.write_data(normalizer.normalized_data)
```

## Understanding the Output

### What You Get

After normalization, each job posting becomes a flat record with ~50+ columns:

```
Row 1 (Headers):
job_id | job_title | source | company_name | job_location | salary_min | salary_max | ...

Row 2 (Sample Naukri Job):
071025028445 | IT Support Engineer | Naukri | Frontier | Coimbatore | 125000 | 200000 | ...

Row 3 (Sample LinkedIn Job):
3692563200 | Data Labeling Analyst | LinkedIn | Facebook | Los Angeles | $19 | $17 | ...

Row 4 (Sample Indeed Job):
1e6e49448374145b | Support Representative | Indeed | AHA | Dallas | 250 | 350 | ...
```

### Key Improvements Over Previous Version

**Before (Old Normalizer):**

```json
[
  {
    "id": "job123",
    "title": "Engineer",
    "url": "...",
    "source": "Naukri",
    "raw_data": {
      "jobId": "job123",
      "title": "Engineer",
      "companyDetail": { ... nested 10 levels deep ... },
      "salaryDetail": { ... },
      "keySkills": { ... }
    }
  }
]
```

❌ Most data is in nested `raw_data` field
❌ Hard to work with in Excel
❌ Can't filter or sort by most fields

**After (New Normalizer):**

```json
[
  {
    "job_id": "job123",
    "job_title": "Engineer",
    "source": "Naukri",
    "company_name": "Frontier",
    "job_location": "Coimbatore",
    "salary_min": 125000,
    "salary_max": 200000,
    "salary_currency": "INR",
    "required_skills": "OS Installation, Outlook Configuration",
    "preferred_skills": "Windows Installation, Ticketing Tools",
    "min_experience_years": 0,
    "max_experience_years": 2,
    "... 40+ more flat fields ..."
  }
]
```

✅ All data in individual columns
✅ Perfect for Excel export
✅ Easy to filter, sort, analyze
✅ One row per job

## Source Detection

The normalizer automatically detects the source based on unique fields:

| Field Indicator                | Source   |
| ------------------------------ | -------- |
| `jobKey` present               | Indeed   |
| `link` contains 'linkedin.com' | LinkedIn |
| `trackingId` present           | LinkedIn |
| `jobId` present                | Naukri   |

If none match, the job is skipped (unknown format).

## Handling Missing Fields

For fields that don't exist in a source:

- Numeric fields default to `0` or empty string
- Text fields default to empty string `""`
- Lists default to empty string (no items)
- URLs default to empty string
- Dates default to empty string

Example: LinkedIn jobs won't have `job_vacancies` (Naukri-only field) → shown as empty in Excel.

## Working with Excel Output

### Filtering

Once exported to Excel, you can easily:

1. **Filter by Source:**
   - Data → Filter → Filter by "Indeed", "LinkedIn", or "Naukri"

2. **Filter by Location:**
   - Apply AutoFilter → job_location column

3. **Filter by Salary Range:**
   - Custom Filter: salary_min ≥ 100000

4. **Filter by Experience:**
   - Filter: min_experience_years ≤ 2

### Sorting

- Sort by `posted_date` to find newest jobs
- Sort by `salary_max` to find highest paying positions
- Sort by `company_rating` to find top-rated companies
- Sort by `source` to group by platform

### Analysis

- Use VLOOKUP to find jobs by ID
- Create pivot tables by `source`, `industry`, `job_role`
- Calculate average salary by location
- Count jobs by company
- Analyze required skills across all jobs

## Field Reference

### Most Important Fields

```
job_id              → Unique identifier
job_title           → Position title
company_name        → Company hiring
job_location        → Where job is located
source              → Which platform (Indeed/LinkedIn/Naukri)
```

### Salary Fields

```
salary_min          → Minimum pay
salary_max          → Maximum pay
salary_currency     → Currency (USD, INR, etc.)
salary_type         → Period (hourly, monthly, annual)
salary_text         → Human-readable (e.g., "1.25-2 Lacs PA")
```

### Experience Fields

```
min_experience_years → Minimum required experience
max_experience_years → Maximum acceptable experience
experience_text      → Human-readable (e.g., "0-2 Yrs")
seniority_level      → LinkedIn: Associate, Senior, etc.
```

### Skills Fields

```
required_skills     → Must-have skills
preferred_skills    → Nice-to-have skills
all_skills          → Combined list of all skills
all_requirements    → All requirements combined
attributes          → Indeed-specific tags/attributes
```

### Company Fields

```
company_name        → Company name
company_logo        → Logo URL
company_website     → Website URL
company_rating      → Overall rating (if available)
company_reviews_count → Number of reviews
company_employees   → Employee count
company_industry    → Industry type
company_description → About company
```

### Location Fields

```
job_location        → Formatted full location
job_city            → City
job_country         → Country
job_latitude        → GPS latitude (Indeed only)
job_longitude       → GPS longitude (Indeed only)
job_street_address  → Street address (Indeed only)
job_postal_code     → ZIP/Postal code (Indeed only)
```

## Examples

### Example 1: Filter High-Paying Remote Jobs

```
Filter: source = "Indeed"
AND is_remote = true
AND salary_max ≥ 100000

Result: Shows all Indeed remote jobs paying $100k+ max
```

### Example 2: Find Jobs Matching Your Skills

You have skills: "Python" and "AWS"

```
Filter: all_skills contains "Python"
AND all_skills contains "AWS"

Result: Shows all matching jobs across all sources
```

### Example 3: Compare Companies

```
Sort by: company_rating (descending)

Chart: company_name vs average salary_max

Result: See which top-rated companies pay most
```

### Example 4: Job Market Analysis

```
Pivot Table:
  Rows: source, job_role
  Values: Count of jobs, Average salary

Result: See which platforms have most of each role
       and average pay by role and platform
```

## Common Issues & Solutions

### Issue: "Unknown format" jobs are being skipped

**Cause:** Job doesn't have expected fields from any source

**Solution:** Check if you're mixing data from an unknown source. Verify field names match expected schema.

### Issue: Excel shows partial data or empty columns

**Cause:** Field doesn't exist in that source

**Solution:** This is normal. Each source has different fields. Use filters to show only relevant data.

### Issue: Salary values look wrong (e.g., "350" instead of "$350,000")

**Cause:** Indeed stores salary differently based on salaryType

**Solution:** Check `salary_type` field. If hourly, multiply by 2080 for annual equivalent. If monthly, multiply by 12.

### Issue: Skills are blank for some jobs

**Cause:** Source didn't include skills in structured format

**Solution:** Check `job_description` field which contains full text where skills may be mentioned.

### Issue: Duplicate jobs appearing

**Cause:** Same job posted on multiple sources

**Solution:** De-duplicate by `job_title` + `company_name` + `job_location` across sources.

## Programmatic Usage

### Get Available Columns

```python
from src.data_normalizer import DataNormalizer

normalizer = DataNormalizer()
normalizer.load_from_json('normalized_data.json')

columns = normalizer.get_unified_columns()
print(columns)
# Output: ['job_id', 'job_title', 'job_url', 'source', 'posted_date', ...]
```

### Access Individual Jobs

```python
first_job = normalizer.normalized_data[0]
print(first_job['job_title'])
print(first_job['company_name'])
print(first_job['salary_max'])
```

### Filter Jobs Programmatically

```python
# Get all Indeed jobs paying more than $100k
high_paying = [
    job for job in normalizer.normalized_data
    if job['source'] == 'Indeed' and int(job['salary_max']) > 100000
]

print(f"Found {len(high_paying)} high-paying Indeed jobs")
```

### Export Specific Fields

```python
import pandas as pd

df = pd.DataFrame(normalizer.normalized_data)

# Export only specific columns
summary = df[['job_id', 'job_title', 'company_name', 'salary_min', 'salary_max', 'source']]
summary.to_excel('job_summary.xlsx', index=False)
```

## Integration with LLM Filter

The new flat schema works perfectly with the LLM filter:

```python
from src.llm_filter import LLMFilter
from src.data_normalizer import DataNormalizer

normalizer = DataNormalizer()
normalizer.load_from_json('normalized_data.json')

llm_filter = LLMFilter()

# Filter normalized data
filtered = llm_filter.filter_jobs(normalizer.normalized_data)

# Write filtered results
from src.excel_writer import ExcelWriter
excel = ExcelWriter('filtered_jobs.xlsx')
excel.write_data(filtered)
```

All fields are flat and easily accessible to the LLM filter!
