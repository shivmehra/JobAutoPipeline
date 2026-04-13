# Quick Reference Card - Unified Job Schema

## Most-Used Fields

### Critical Fields (In Every Record)

```
job_id              → Unique job identifier
job_title           → Position title
company_name        → Hiring company
job_location        → Job location
source              → Naukri, LinkedIn, or Indeed
posted_date         → When job was posted
```

### Key Business Fields

```
salary_min          → Minimum pay
salary_max          → Maximum pay
salary_currency     → Currency (INR, USD)
salary_type         → hourly / monthly / annual
required_skills     → Must-have skills
job_description     → Full job description
employment_type     → Full-time, Contract, etc.
```

### Additional Important Fields

```
job_url                → Link to job posting
company_website        → Company website
company_rating         → Company rating (1-5)
min_experience_years   → Min experience required
max_experience_years   → Max experience required
job_role               → Specific role name
industry               → Industry type
job_vacancies          → Number of openings
is_remote              → True/False for remote work
```

## Common Filtering Examples

### Find Jobs by Experience

```
Filter: min_experience_years ≤ 2
AND max_experience_years ≥ 0
= Entry-level jobs
```

### Find Jobs by Location

```
Filter: job_country = "India"
OR job_country = "USA"
```

### Find High-Paying Jobs

```
Filter: salary_currency = "USD"
AND salary_max > 100000
```

### Find Remote Jobs with Skills

```
Filter: is_remote = True
AND (required_skills contains "Python"
  OR required_skills contains "Java")
```

### Find Specific Role at Top Companies

```
Filter: job_role = "Backend Engineer"
AND company_rating > 4.0
```

## Common Sorting Examples

```
Sort by posted_date DESC           → Newest jobs first
Sort by salary_max DESC             → Highest paying first
Sort by company_rating DESC         → Top-rated companies
Sort by job_location ASC            → Group by location
Sort by source ASC                  → Group by platform
```

## Excel Tips

### Quick Filters

1. Select header row
2. Data → AutoFilter
3. Click dropdown in any column
4. Select/deselect values
5. Click OK

### Create Salary Range

```
Create new column: salary_avg = (salary_max + salary_min) / 2
```

### Convert Salary to Annual (for hourly rates)

```
Create new column: salary_annual = salary_max * 2080
(Or multiply by 1920 for conservative estimate)
```

### Find Salary by Location

```
Pivot Table:
  Rows: job_location
  Values: Average(salary_max)
```

### Show Only Jobs You're Qualified For

```
Filter: min_experience_years ≤ (your_experience)
AND (your_skills found in required_skills)
```

## Column Categories Cheat Sheet

### Job Info (7 columns)

`job_id`, `job_title`, `job_url`, `source`, `posted_date`, `job_description`, `job_type`

### Company (11 columns)

`company_name`, `company_logo`, `company_website`, `company_rating`, `company_reviews_count`,
`company_employees`, `company_revenue`, `company_industry`, `company_founded_year`,
`company_description`, `company_ceo`

### Location (7 columns)

`job_location`, `job_city`, `job_country`, `job_latitude`, `job_longitude`,
`job_street_address`, `job_postal_code`

### Salary (5 columns)

`salary_min`, `salary_max`, `salary_currency`, `salary_text`, `salary_type`

### Experience (4 columns)

`min_experience_years`, `max_experience_years`, `experience_text`, `seniority_level`

### Skills (5 columns)

`required_skills`, `preferred_skills`, `all_skills`, `all_requirements`, `attributes`

### Education (2 columns)

`education_ug`, `education_pg`

### Other Info (remaining ~15+ columns)

`job_role`, `role_category`, `industry`, `functional_area`, `job_vacancies`,
`employment_type`, `job_function`, `occupation`, `benefits`, `is_remote`, etc.

## Handling Missing Data

| Field Type | Missing Value                   |
| ---------- | ------------------------------- |
| Numbers    | 0 or empty                      |
| Text       | empty string `""`               |
| URLs       | empty string `""`               |
| Lists      | empty string or comma-separated |
| Boolean    | False or empty                  |
| Dates      | empty string                    |

**Note**: Fields specific to one source will be empty in others (e.g., `job_vacancies` is Naukri-only)

## Source-Specific Fields

### Naukri-Only Fields

- `job_role`, `role_category`, `functional_area`, `education_ug`, `education_pg`
- `apply_count`, `view_count`, `job_vacancies`, `wfh_type`

### LinkedIn-Only Fields

- `seniority_level`, `recruiter_name`, `recruiter_title`, `recruiter_profile`

### Indeed-Only Fields

- `is_urgent_hire`, `job_latitude`, `job_longitude`, `job_street_address`
- `company_revenue`, `company_founded_year`, `company_ceo`, `candidates_count`
- `total_applicants`, `shift_schedule`, `working_system`

## Python Quick Code Snippets

### Load and Inspect

```python
from src.data_normalizer import DataNormalizer
normalizer = DataNormalizer()
normalizer.load_from_json('normalized_data.json')
print(len(normalizer.normalized_data))  # Count of jobs
print(list(normalizer.normalized_data[0].keys()))  # All columns
```

### Filter Programmatically

```python
# Get engineering jobs paying >$150k
filtered = [j for j in normalizer.normalized_data
            if 'Engineer' in j.get('job_title', '')
            and int(j.get('salary_max', 0)) > 150000]
```

### Get Statistics

```python
import pandas as pd
df = pd.DataFrame(normalizer.normalized_data)
print(df['salary_max'].mean())  # Average max salary
print(df['source'].value_counts())  # Jobs per source
print(df['job_location'].value_counts().head())  # Top locations
```

### Export Specific Columns

```python
df = pd.DataFrame(normalizer.normalized_data)
subset = df[['job_title', 'company_name', 'salary_min', 'salary_max', 'job_location']]
subset.to_excel('summary.xlsx', index=False)
```

## Data Quality Checks

### Find Missing Salary

```
Filter: (salary_min is empty OR salary_min = "")
Result: Shows jobs without salary info
```

### Find Short Descriptions

```
Create formula: =LEN(job_description)
Filter: < 100 characters
Result: Show jobs with very short descriptions
```

### Check Data Completeness

```
For each column, count non-empty values
Identify which fields have most missing data
```

## Integration with LLM Filter

All fields are accessible and filterable:

```python
from src.llm_filter import LLMFilter
normalizer.load_from_json()
llm = LLMFilter()
filtered = llm.filter_jobs(normalizer.normalized_data)
```

LLM can use any field to make decisions about job suitability!

## Troubleshooting

**Q: Why is a column empty for all rows?**
A: That field might be source-specific. Check which sources provide it.

**Q: Why are salaries different formats?**
A: Different sources use different units (hourly vs annual). Check `salary_type`.

**Q: Can I merge/deduplicate jobs?**
A: Yes! Use: `job_title + company_name + job_location` as unique key.

**Q: How do I update salary for hourly to annual?**
A: Multiply by 2080 (standard working hours per year).

**Q: Why can't I filter by salary on some jobs?**
A: Some jobs have `salary_text` but not numeric `salary_min`/`salary_max`. Parse the text manually or leave as is.

---

**Need more help?** See the full documentation:

- [UNIFIED_SCHEMA.md](UNIFIED_SCHEMA.md) - All fields explained
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Complete guide
- [SCHEMA_TRANSFORMATION_EXAMPLES.md](SCHEMA_TRANSFORMATION_EXAMPLES.md) - Real examples
