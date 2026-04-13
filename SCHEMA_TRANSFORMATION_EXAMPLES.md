# Schema Transformation Examples

This document shows how job postings from each source are transformed into the unified schema.

## Example 1: Naukri → Unified Schema

### Naukri Source Data (Relevant Fields)

```json
{
  "jobId": "071025028445",
  "title": "It Support Engineer",
  "staticUrl": "https://www.naukri.com/job-listings-it-support-engineer",
  "description": "<p>Provide first-level support...</p>",
  "short_description": "Experience in IT support...",
  "createdDate": "2025-10-07 17:31:13",
  "employmentType": "Full Time, Permanent",
  "companyDetail": {
    "name": "Frontier",
    "websiteUrl": "",
    "details": "<p>Frontier with over 30 years...</p>"
  },
  "banner": "https://img.naukimg.com/logo_images/groups/v1/mobile/4596369.gif",
  "locations": [
    {
      "label": "Coimbatore",
      "url": "https://www.naukri.com/jobs-in-coimbatore"
    }
  ],
  "salaryDetail": {
    "minimumSalary": 125000,
    "maximumSalary": 200000,
    "currency": "INR",
    "label": "1.25-2 Lacs"
  },
  "experienceText": "0-2 Yrs",
  "minimumExperience": 0,
  "maximumExperience": 2,
  "jobRole": "Desktop Engineer",
  "roleCategory": "IT Support",
  "functionalArea": "IT & Information Security",
  "industry": "Industrial Equipment / Machinery",
  "vacancy": 3,
  "keySkills": {
    "preferred": [
      { "label": "OS Installation" },
      { "label": "Outlook Configuration" }
    ],
    "other": [
      { "label": "Windows Installation" },
      { "label": "Ticketing Tools" }
    ]
  },
  "education": {
    "ug": ["Any Graduate"],
    "pg": []
  },
  "applyCount": 362,
  "viewCount": 1136,
  "wfhType": "0",
  "ambitionBoxDetails": {
    "companyInfo": {
      "AggregateRating": "3.4",
      "ReviewsCount": "136"
    }
  }
}
```

### Normalized Output (Unified Schema)

```json
{
  "job_id": "071025028445",
  "job_title": "It Support Engineer",
  "job_url": "https://www.naukri.com/job-listings-it-support-engineer",
  "source": "Naukri",
  "posted_date": "2025-10-07 17:31:13",
  "job_description": "Provide first-level support...",
  "job_type": "Full Time, Permanent",
  "company_name": "Frontier",
  "company_logo": "https://img.naukimg.com/logo_images/groups/v1/mobile/4596369.gif",
  "company_website": "",
  "company_rating": "3.4",
  "company_reviews_count": 136,
  "job_location": "Coimbatore",
  "job_country": "India",
  "salary_min": 125000,
  "salary_max": 200000,
  "salary_currency": "INR",
  "salary_text": "1.25-2 Lacs",
  "salary_type": "annual",
  "min_experience_years": 0,
  "max_experience_years": 2,
  "experience_text": "0-2 Yrs",
  "job_role": "Desktop Engineer",
  "role_category": "IT Support",
  "functional_area": "IT & Information Security",
  "industry": "Industrial Equipment / Machinery",
  "job_vacancies": 3,
  "required_skills": "OS Installation, Outlook Configuration",
  "preferred_skills": "Windows Installation, Ticketing Tools",
  "all_skills": "OS Installation, Outlook Configuration, Windows Installation, Ticketing Tools",
  "education_ug": "Any Graduate",
  "education_pg": "",
  "apply_count": 362,
  "view_count": 1136,
  "wfh_type": "0"
}
```

---

## Example 2: LinkedIn → Unified Schema

### LinkedIn Source Data (Relevant Fields)

```json
{
  "id": "3692563200",
  "title": "English Data Labeling Analyst",
  "link": "https://www.linkedin.com/jobs/view/english-data-labeling-analyst-at-facebook-3692563200",
  "companyName": "Facebook",
  "companyLinkedinUrl": "https://www.linkedin.com/company/facebook",
  "companyLogo": "https://media.licdn.com/dms/image/...",
  "location": "Los Angeles Metropolitan Area",
  "postedAt": "2023-08-16",
  "descriptionText": "APPROVED REMOTE LOCATIONS:...",
  "benefits": ["Actively Hiring"],
  "salaryInfo": ["$17.00", "$19.00"],
  "seniorityLevel": "Associate",
  "employmentType": "Contract",
  "jobFunction": "Other",
  "industries": "Retail Office Equipment",
  "companyDescription": "The Facebook company is now Meta...",
  "companyWebsite": "https://www.meta.com",
  "companyEmployeesCount": 36275,
  "applicantsCount": "200",
  "jobPosterName": "Andrea Cowan",
  "jobPosterTitle": "Technical Recruiter at Meta",
  "jobPosterProfileUrl": "https://ca.linkedin.com/in/andrea-cowan"
}
```

### Normalized Output (Unified Schema)

```json
{
  "job_id": "3692563200",
  "job_title": "English Data Labeling Analyst",
  "job_url": "https://www.linkedin.com/jobs/view/english-data-labeling-analyst-at-facebook-3692563200",
  "source": "LinkedIn",
  "posted_date": "2023-08-16",
  "job_description": "APPROVED REMOTE LOCATIONS:...",
  "job_type": "Actively Hiring",
  "company_name": "Facebook",
  "company_logo": "https://media.licdn.com/dms/image/...",
  "company_website": "https://www.meta.com",
  "company_employees": 36275,
  "company_description": "The Facebook company is now Meta...",
  "job_location": "Los Angeles Metropolitan Area",
  "job_country": "USA",
  "salary_min": "$19.00",
  "salary_max": "$17.00",
  "salary_currency": "USD",
  "salary_text": "$17.00 - $19.00",
  "salary_type": "hourly",
  "seniority_level": "Associate",
  "employment_type": "Contract",
  "job_function": "Other",
  "industries": "Retail Office Equipment",
  "recruiter_name": "Andrea Cowan",
  "recruiter_title": "Technical Recruiter at Meta",
  "recruiter_profile": "https://ca.linkedin.com/in/andrea-cowan",
  "applicants_count": "200"
}
```

---

## Example 3: Indeed → Unified Schema

### Indeed Source Data (Relevant Fields)

```json
{
  "title": "Remote Customer Support Representative",
  "jobKey": "1e6e49448374145b",
  "jobUrl": "https://www.indeed.com/viewjob?jk=6ae7e4ae7ac60636",
  "companyName": "American Heart Association",
  "companyLogoUrl": "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/...",
  "isRemote": true,
  "jobType": ["Full-time", "Remote"],
  "descriptionText": "Provide tier I technical support...",
  "datePublished": "2025-02-24",
  "location": {
    "countryCode": "US",
    "country": "United States",
    "city": "Dallas",
    "formattedAddressShort": "Dallas, TX",
    "formattedAddressLong": " Dallas, Texas 75231-4596, US",
    "postalCode": "75231",
    "latitude": 32.814034,
    "longitude": -96.815,
    "streetAddress": "7272 Greenville Ave."
  },
  "salary": {
    "salaryText": "$20 - $22 an hour",
    "salaryType": "hourly",
    "salaryMax": 350,
    "salaryMin": 250,
    "salaryCurrency": "USD"
  },
  "rating": {
    "rating": 3.9,
    "count": 885
  },
  "companyNumEmployees": "1,001 to 5,000",
  "companyRevenue": "$500M to $1B (USD)",
  "companyIndustry": "ASSOCIATION",
  "companyDescription": "The American Heart Association is a relentless force...",
  "companyFounded": {
    "year": 1924
  },
  "benefits": ["Health insurance", "Paid time off", "Retirement plan"],
  "occupation": ["Customer Support & Client Services Occupations"],
  "requirements": [
    { "label": "Engineering", "requirementSeverity": "REQUIRED" },
    { "label": "Associate's degree", "requirementSeverity": "PREFERRED" }
  ],
  "shiftAndSchedule": ["Monday to Friday"],
  "workingSystem": ["Flextime"],
  "attributes": ["Bilingual", "Microsoft Word", "Spanish"],
  "hiringDemand": {
    "isUrgentHire": true,
    "isHighVolumeHiring": false
  },
  "numOfCandidates": 3,
  "organicApplyStarts": 11,
  "companyUrl": "https://www.indeed.com/cmp/American-Heart-Association",
  "companyLinks": {
    "facebook": "https://www.facebook.com/theahalife",
    "instagram": "https://www.instagram.com/theahalife",
    "corporateWebsite": "http://www.heart.org"
  },
  "companyCeo": {
    "name": "Nancy A. Brown"
  }
}
```

### Normalized Output (Unified Schema)

```json
{
  "job_id": "1e6e49448374145b",
  "job_title": "Remote Customer Support Representative",
  "job_url": "https://www.indeed.com/viewjob?jk=6ae7e4ae7ac60636",
  "source": "Indeed",
  "posted_date": "2025-02-24",
  "job_description": "Provide tier I technical support...",
  "job_type": "Full-time, Remote",
  "is_remote": true,
  "is_urgent_hire": true,
  "company_name": "American Heart Association",
  "company_logo": "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/...",
  "company_website": "http://www.heart.org",
  "company_employees": "1,001 to 5,000",
  "company_revenue": "$500M to $1B (USD)",
  "company_industry": "ASSOCIATION",
  "company_founded_year": 1924,
  "company_description": "The American Heart Association is a relentless force...",
  "company_rating": 3.9,
  "company_rating_count": 885,
  "company_ceo": "Nancy A. Brown",
  "job_location": "Dallas, TX",
  "job_city": "Dallas",
  "job_country": "United States",
  "job_latitude": 32.814034,
  "job_longitude": -96.815,
  "job_street_address": "7272 Greenville Ave.",
  "job_postal_code": "75231",
  "salary_min": 250,
  "salary_max": 350,
  "salary_currency": "USD",
  "salary_text": "$20 - $22 an hour",
  "salary_type": "hourly",
  "occupation": "Customer Support & Client Services Occupations",
  "shift_schedule": "Monday to Friday",
  "working_system": "Flextime",
  "required_skills": "Engineering",
  "preferred_skills": "Associate's degree",
  "all_requirements": "Engineering, Associate's degree",
  "attributes": "Bilingual, Microsoft Word, Spanish",
  "benefits": "Health insurance, Paid time off, Retirement plan",
  "candidates_count": 3,
  "total_applicants": 11
}
```

---

## Key Transformation Patterns

### Salary Handling

- **Naukri**: Annual salary in local currency (INR)
- **LinkedIn**: Hourly rate in USD, value appears in `salaryInfo` array
- **Indeed**: Flexible - can be hourly, salary, or other types
- **Unified**: All mapped to `salary_min`, `salary_max`, `salary_currency`, `salary_type`

### Skills Extraction

- **Naukri**: Nested array with `preferred` and `other` skills
- **LinkedIn**: Text embedded in description
- **Indeed**: Requirements with severity levels (REQUIRED, PREFERRED)
- **Unified**: Separated into `required_skills`, `preferred_skills`, `all_skills`

### Location Handling

- **Naukri**: Single location string or array
- **LinkedIn**: Single formatted string
- **Indeed**: Complete nested object with coordinates
- **Unified**: Flat structure with individual fields for city, country, coordinates

### Company Info

- **Naukri**: Basic company details + AmbitionBox ratings
- **LinkedIn**: Company info + employee count + CEO info
- **Indeed**: Comprehensive company data including founding year, revenue, CEO
- **Unified**: All standardized into 10+ company-related fields

### Date Format

- **Naukri**: DateTime string "YYYY-MM-DD HH:MM:SS"
- **LinkedIn**: Date string "YYYY-MM-DD"
- **Indeed**: Date string "YYYY-MM-DD"
- **Unified**: Kept as-is in `posted_date` field

## Using Normalized Data in Excel

Once normalized, all records fit into a consistent columnar structure:

| job_id           | job_title              | company_name | job_location | salary_min | salary_max | salary_currency | source   |
| ---------------- | ---------------------- | ------------ | ------------ | ---------- | ---------- | --------------- | -------- |
| 071025028445     | IT Support Engineer    | Frontier     | Coimbatore   | 125000     | 200000     | INR             | Naukri   |
| 3692563200       | Data Labeling Analyst  | Facebook     | Los Angeles  | $19        | $17        | USD             | LinkedIn |
| 1e6e49448374145b | Support Representative | AHA          | Dallas, TX   | 250        | 350        | USD             | Indeed   |

Each column can be sorted, filtered, and analyzed independently without needing to parse nested JSON structures.
