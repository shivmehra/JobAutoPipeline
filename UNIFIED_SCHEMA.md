# Unified Job Schema Documentation

This document describes the normalized schema used to standardize job postings from Naukri, LinkedIn, and Indeed into a single flat structure for Excel export.

## Schema Overview

All job postings are normalized into the following columns:

### Basic Job Information

- `job_id` - Unique job identifier from source
- `job_title` - Job position title
- `job_url` - Link to job posting
- `source` - Source platform (Naukri, LinkedIn, Indeed)
- `posted_date` - Date job was posted
- `job_description` - Full job description text
- `job_type` - Full-time, Part-time, Contract, Intern, etc.

### Company Information

- `company_name` - Name of hiring company
- `company_logo` - URL to company logo
- `company_website` - Company website URL
- `company_rating` - Overall company rating (if available)
- `company_reviews_count` - Number of company reviews
- `company_employees` - Number of employees
- `company_revenue` - Annual revenue (Indeed only)
- `company_industry` - Industry classification
- `company_founded_year` - Year company was founded
- `company_description` - Company description text
- `company_ceo` - CEO name (Indeed only)

### Location Information

- `job_location` - Formatted location string (e.g., "Mumbai, Maharashtra" or "New York, NY")
- `job_city` - City name
- `job_country` - Country
- `job_latitude` - GPS latitude (Indeed only)
- `job_longitude` - GPS longitude (Indeed only)
- `job_street_address` - Street address (Indeed only)
- `job_postal_code` - Postal/ZIP code (Indeed only)

### Compensation

- `salary_min` - Minimum salary
- `salary_max` - Maximum salary
- `salary_currency` - Currency (USD, INR, etc.)
- `salary_text` - Human-readable salary label (e.g., "1.25-2 Lacs PA")
- `salary_type` - Salary period (hourly, monthly, annual)

### Experience Requirements

- `min_experience_years` - Minimum years of experience required
- `max_experience_years` - Maximum years of experience
- `experience_text` - Human-readable experience label (e.g., "0-2 Yrs")
- `seniority_level` - Seniority level (LinkedIn only: Associate, Senior, etc.)

### Job Details

- `job_role` - Specific job role (Naukri only)
- `role_category` - Role category (Naukri only)
- `functional_area` - Functional area of the role (Naukri only)
- `industry` - Industry type
- `job_vacancies` - Number of open positions (Naukri only)
- `employment_type` - Employment type classification (Naukri only)
- `job_function` - Job function category (LinkedIn only)
- `occupation` - Occupation category (Indeed only)

### Skills & Requirements

- `required_skills` - Required skills (comma-separated)
- `preferred_skills` - Preferred/nice-to-have skills (comma-separated)
- `all_skills` - All mentioned skills combined
- `all_requirements` - All requirements combined
- `attributes` - Job attributes/tags (Indeed only)

### Education Requirements

- `education_ug` - Undergraduate degree requirements (Naukri only)
- `education_pg` - Postgraduate degree requirements (Naukri only)

### Benefits & Perks

- `benefits` - Benefits offered (comma-separated)
- `social_insurance` - Insurance and social benefits (Indeed only)

### Work Arrangement

- `is_remote` - Whether job is remote (Indeed only)
- `wfh_type` - Work from home type (Naukri only: 0=No, 1=Yes)
- `shift_schedule` - Work shift schedule (Indeed only)
- `working_system` - Working system (Indeed only: Flextime, etc.)

### Additional Information

- `apply_count` - Number of applications (Naukri only)
- `view_count` - Number of views (Naukri only)
- `is_urgent_hire` - Urgent hiring indicator (Indeed only)
- `candidates_count` - Number of candidates (Indeed only)
- `total_applicants` - Total applicants (Indeed only)
- `recruiter_name` - Name of recruiter posting job (LinkedIn only)
- `recruiter_title` - Recruiter's job title (LinkedIn only)
- `recruiter_profile` - Recruiter profile URL (LinkedIn only)

## Schema Mapping by Source

### Naukri Fields

Maps from the full Naukri job posting schema to unified schema:

- Title → job_title
- jobId → job_id
- description/shortDescription → job_description
- employmentType → job_type
- companyDetail.name → company_name
- education.ug/pg → education_ug/pg
- keySkills.preferred/other → required_skills/preferred_skills
- salaryDetail → salary_min/max/currency/text
- locations[0] → job_location

### LinkedIn Fields

Maps from LinkedIn job posting schema:

- title → job_title
- id → job_id
- link → job_url
- descriptionText → job_description
- companyName → company_name
- location → job_location
- salaryInfo → salary_min/max
- seniorityLevel → seniority_level
- benefitsText → job_type

### Indeed Fields

Maps from Indeed job posting schema:

- title → job_title
- jobKey → job_id
- jobUrl → job_url
- descriptionText → job_description
- companyName → company_name
- location → job_location/city/country/coordinates
- salary → salary_min/max/currency/type
- jobType → job_type
- requirements → required/preferred_skills
- rating.rating → company_rating
- hiringDemand.isUrgentHire → is_urgent_hire

## Usage Example

After normalization, a single job record might look like:

```json
{
  "job_id": "071025028445",
  "job_title": "IT Support Engineer",
  "job_url": "https://www.naukri.com/job-listings-it-support-engineer",
  "source": "Naukri",
  "posted_date": "2025-10-07",
  "job_description": "Provide first-level support for desktop...",
  "job_type": "Full Time, Permanent",
  "company_name": "Frontier",
  "job_location": "Coimbatore",
  "job_country": "India",
  "salary_min": 125000,
  "salary_max": 200000,
  "salary_currency": "INR",
  "salary_type": "annual",
  "min_experience_years": 0,
  "max_experience_years": 2,
  "experience_text": "0-2 Yrs",
  "required_skills": "OS Installation, Outlook Configuration",
  "preferred_skills": "Windows Installation, Ticketing Tools",
  "benefits": "Health insurance, Cafeteria",
  ...
}
```

## Excel Export Behavior

When normalized data is exported to Excel:

- Each record becomes one row
- Each field becomes a column
- No nested data - all values are flat strings or numbers
- Empty/missing fields are represented as empty strings
- Comma-separated lists are used for multi-value fields
- This ensures maximum compatibility with Excel and other tools
