# Data normalizer for Apify actor results
import json

class DataNormalizer:
    def __init__(self):
        self.normalized_data = []

    def _safe_get(self, obj, keys, default=''):
        """Safely get nested values from dict"""
        if isinstance(keys, list):
            for key in keys:
                if isinstance(obj, dict):
                    obj = obj.get(key)
                else:
                    return default
            return obj if obj is not None else default
        return obj.get(keys, default) if isinstance(obj, dict) else default

    def _normalize_naukri(self, item):
        """Normalize Naukri job posting"""
        skills = item.get('keySkills', {})
        preferred_skills = skills.get('preferred', [])
        other_skills = skills.get('other', [])
        
        # Combine skills
        all_skills = [s.get('label', '') for s in preferred_skills + other_skills]
        preferred_skill_labels = [s.get('label', '') for s in preferred_skills]
        
        company_detail = item.get('companyDetail', {})
        location = item.get('locations', [{}])[0] if item.get('locations') else {}
        salary = item.get('salaryDetail', {})
        ambition_box = item.get('ambitionBoxDetails', {})
        company_info = ambition_box.get('companyInfo', {})
        
        normalized = {
            # Basic Info
            'job_id': item.get('jobId', ''),
            'job_title': item.get('title', ''),
            'job_url': item.get('staticUrl', ''),
            'source': 'Naukri',
            'posted_date': item.get('createdDate', ''),
            'job_description': item.get('description', item.get('shortDescription', '')),
            'job_type': item.get('employmentType', ''),
            
            # Company Info
            'company_name': company_detail.get('name', ''),
            'company_logo': item.get('banner', ''),
            'company_website': company_detail.get('websiteUrl', ''),
            'company_rating': company_info.get('AggregateRating', ''),
            'company_reviews_count': company_info.get('ReviewsCount', 0),
            
            # Location
            'job_location': location.get('label', ''),
            'job_country': 'India',
            
            # Salary Info
            'salary_min': salary.get('minimumSalary', ''),
            'salary_max': salary.get('maximumSalary', ''),
            'salary_currency': salary.get('currency', 'INR'),
            'salary_text': salary.get('label', ''),
            'salary_type': 'annual',
            
            # Experience
            'min_experience_years': item.get('minimumExperience', 0),
            'max_experience_years': item.get('maximumExperience', 0),
            'experience_text': item.get('experienceText', ''),
            
            # Job Details
            'job_role': item.get('jobRole', ''),
            'role_category': item.get('roleCategory', ''),
            'functional_area': item.get('functionalArea', ''),
            'industry': item.get('industry', ''),
            'job_vacancies': item.get('vacancy', 0),
            
            # Skills
            'required_skills': ', '.join(preferred_skill_labels) if preferred_skill_labels else '',
            'preferred_skills': ', '.join([s.get('label', '') for s in other_skills]) if other_skills else '',
            'all_skills': ', '.join(all_skills) if all_skills else '',
            
            # Education
            'education_ug': ', '.join(item.get('education', {}).get('ug', [])),
            'education_pg': ', '.join(item.get('education', {}).get('pg', [])),
            
            # Additional
            'apply_count': item.get('applyCount', 0),
            'view_count': item.get('viewCount', 0),
            'wfh_type': item.get('wfhType', ''),
        }
        return normalized

    def _normalize_linkedin(self, item):
        """Normalize LinkedIn job posting"""
        salary_info = item.get('salaryInfo', [])
        salary_min = salary_info[1] if len(salary_info) > 1 else ''
        salary_max = salary_info[0] if len(salary_info) > 0 else ''
        
        normalized = {
            # Basic Info
            'job_id': item.get('id', ''),
            'job_title': item.get('title', ''),
            'job_url': item.get('link', ''),
            'source': 'LinkedIn',
            'posted_date': item.get('postedAt', ''),
            'job_description': item.get('descriptionText', ''),
            'job_type': ', '.join(item.get('benefits', [])) if item.get('benefits') else '',
            
            # Company Info
            'company_name': item.get('companyName', ''),
            'company_logo': item.get('companyLogo', ''),
            'company_website': item.get('companyWebsite', ''),
            'company_employees': item.get('companyEmployeesCount', ''),
            'company_description': item.get('companyDescription', ''),
            
            # Location
            'job_location': item.get('location', ''),
            'job_country': 'USA',
            
            # Salary Info
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': 'USD',
            'salary_text': f"${salary_max} - ${salary_min}" if salary_min and salary_max else '',
            'salary_type': 'hourly',
            
            # Experience
            'seniority_level': item.get('seniorityLevel', ''),
            'employment_type': item.get('employmentType', ''),
            'job_function': item.get('jobFunction', ''),
            
            # Job Details
            'industries': item.get('industries', ''),
            
            # Recruiter Info
            'recruiter_name': item.get('jobPosterName', ''),
            'recruiter_title': item.get('jobPosterTitle', ''),
            'recruiter_profile': item.get('jobPosterProfileUrl', ''),
            
            # Additional
            'applicants_count': item.get('applicantsCount', 0),
        }
        return normalized

    def _normalize_indeed(self, item):
        """Normalize Indeed job posting"""
        location = item.get('location', {})
        salary = item.get('salary', {})
        company_links = item.get('companyLinks', {})
        requirements = item.get('requirements', [])
        
        # Extract requirement labels
        requirement_labels = [r.get('label', '') for r in requirements]
        
        required_reqs = [r.get('label', '') for r in requirements if r.get('requirementSeverity') == 'REQUIRED']
        preferred_reqs = [r.get('label', '') for r in requirements if r.get('requirementSeverity') == 'PREFERRED']
        
        normalized = {
            # Basic Info
            'job_id': item.get('jobKey', ''),
            'job_title': item.get('title', ''),
            'job_url': item.get('jobUrl', ''),
            'source': 'Indeed',
            'posted_date': item.get('datePublished', ''),
            'job_description': item.get('descriptionText', ''),
            'job_type': ', '.join(item.get('jobType', [])) if item.get('jobType') else '',
            'is_remote': item.get('isRemote', False),
            'is_urgent_hire': item.get('hiringDemand', {}).get('isUrgentHire', False),
            
            # Company Info
            'company_name': item.get('companyName', ''),
            'company_logo': item.get('companyLogoUrl', ''),
            'company_website': company_links.get('corporateWebsite', ''),
            'company_employees': item.get('companyNumEmployees', ''),
            'company_revenue': item.get('companyRevenue', ''),
            'company_industry': item.get('companyIndustry', ''),
            'company_founded_year': item.get('companyFounded', {}).get('year', ''),
            'company_description': item.get('companyDescription', ''),
            'company_rating': item.get('rating', {}).get('rating', ''),
            'company_rating_count': item.get('rating', {}).get('count', 0),
            'company_ceo': item.get('companyCeo', {}).get('name', ''),
            
            # Location
            'job_location': location.get('formattedAddressShort', ''),
            'job_city': location.get('city', ''),
            'job_country': location.get('country', ''),
            'job_latitude': location.get('latitude', ''),
            'job_longitude': location.get('longitude', ''),
            'job_street_address': location.get('streetAddress', ''),
            'job_postal_code': location.get('postalCode', ''),
            
            # Salary Info
            'salary_min': salary.get('salaryMin', ''),
            'salary_max': salary.get('salaryMax', ''),
            'salary_currency': salary.get('salaryCurrency', 'USD'),
            'salary_text': salary.get('salaryText', ''),
            'salary_type': salary.get('salaryType', ''),
            
            # Job Details
            'occupation': ', '.join(item.get('occupation', [])) if item.get('occupation') else '',
            'shift_schedule': ', '.join(item.get('shiftAndSchedule', [])) if item.get('shiftAndSchedule') else '',
            'working_system': ', '.join(item.get('workingSystem', [])) if item.get('workingSystem') else '',
            
            # Skills & Requirements
            'required_skills': ', '.join(required_reqs) if required_reqs else '',
            'preferred_skills': ', '.join(preferred_reqs) if preferred_reqs else '',
            'all_requirements': ', '.join(requirement_labels) if requirement_labels else '',
            'attributes': ', '.join(item.get('attributes', [])) if item.get('attributes') else '',
            
            # Benefits
            'benefits': ', '.join(item.get('benefits', [])) if item.get('benefits') else '',
            'social_insurance': ', '.join(item.get('socialInsurance', [])) if item.get('socialInsurance') else '',
            
            # Additional
            'candidates_count': item.get('numOfCandidates', 0),
            'total_applicants': item.get('organicApplyStarts', 0),
        }
        return normalized

    def normalize_actor_data(self, actor_data_list):
        """
        Normalize data from multiple actors into a unified flat schema
        actor_data_list: list of data from different actors
        """
        normalized_items = []

        for actor_data in actor_data_list:
            for item in actor_data:
                # Detect source and normalize accordingly
                if 'jobKey' in item:
                    normalized_item = self._normalize_indeed(item)
                elif 'trackingId' in item or (item.get('link') and 'linkedin.com' in item.get('link', '')):
                    normalized_item = self._normalize_linkedin(item)
                elif 'jobId' in item:
                    normalized_item = self._normalize_naukri(item)
                else:
                    # Fallback - skip unknown format
                    continue

                normalized_items.append(normalized_item)

        self.normalized_data = normalized_items
        return normalized_items

    def deduplicate(self):
        """Remove duplicate jobs based on title + company + location"""
        seen = set()
        unique_data = []
        
        for job in self.normalized_data:
            key = (
                job.get('job_title', ''),
                job.get('company_name', ''),
                job.get('job_location', '')
            )
            
            if key not in seen:
                seen.add(key)
                unique_data.append(job)
        
        original_count = len(self.normalized_data)
        self.normalized_data = unique_data
        duplicates_removed = original_count - len(unique_data)
        
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate jobs ({len(unique_data)} unique jobs remaining)")
        
        return unique_data

    def get_unified_columns(self):
        """Return the unified schema columns"""
        if not self.normalized_data:
            return []
        return list(self.normalized_data[0].keys())

    def save_to_json(self, filename='normalized_data.json'):
        """Save normalized data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.normalized_data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filename='normalized_data.json'):
        """Load normalized data from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            self.normalized_data = json.load(f)
        return self.normalized_data