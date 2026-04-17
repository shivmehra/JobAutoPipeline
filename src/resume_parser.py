# Resume Parser - Extract structured info from resume Word document
import json
from docx import Document
from typing import Dict, List, Any

class ResumeParser:
    """
    Parses a resume from a Word document and extracts structured information.
    Handles unstructured resume text by intelligently identifying sections.
    """
    
    def __init__(self, doc_path: str):
        """Load and parse resume from Word document"""
        self.doc_path = doc_path
        self.raw_text = ""
        self.resume_data = {}
        self._load_document()
    
    def _load_document(self):
        """Load text from Word document"""
        try:
            doc = Document(self.doc_path)
            self.raw_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        except Exception as e:
            print(f"Error loading resume document: {e}")
            self.raw_text = ""
    
    def extract_resume(self) -> Dict[str, Any]:
        """
        Extract and structure resume information.
        Returns dict with keys: skills, experience, education, salary_expectations, career_level, summary
        """
        self.resume_data = {
            'summary': self._extract_summary(),
            'skills': self._extract_skills(),
            'experience': self._extract_experience(),
            'education': self._extract_education(),
            'salary_expectations': self._extract_salary(),
            'career_level': self._extract_career_level(),
            'raw_text': self.raw_text
        }
        return self.resume_data
    
    def _extract_summary(self) -> str:
        """Extract a brief professional summary from resume"""
        lines = self.raw_text.split('\n')
        # Try to get first few lines as summary (before structured sections)
        summary_lines = []
        for line in lines[:10]:  # Check first 10 lines
            lower_line = line.lower()
            # Skip section headers and continue collecting until we hit a section
            if any(keyword in lower_line for keyword in ['skills', 'experience', 'education', 'certification', 'project']):
                break
            if line.strip() and not line.strip().endswith(':'):
                summary_lines.append(line.strip())
        
        return ' '.join(summary_lines[:3])  # First 3 lines as summary
    
    def _extract_skills(self) -> List[str]:
        """Extract skills from resume"""
        skills = []
        text_lower = self.raw_text.lower()
        
        # Find skills section
        skills_start = max(
            text_lower.find('skills'),
            text_lower.find('technical skills'),
            text_lower.find('skill'),
            -1
        )
        
        if skills_start == -1:
            return skills
        
        # Find where skills section ends (next major section)
        section_keywords = ['experience', 'education', 'certification', 'project', 'languages', 'summary']
        skills_end = len(self.raw_text)
        for keyword in section_keywords:
            pos = text_lower.find(keyword, skills_start + 10)
            if pos != -1 and pos < skills_end:
                skills_end = pos
        
        skills_section = self.raw_text[skills_start:skills_end]
        
        # Extract skills (usually comma or newline separated)
        for line in skills_section.split('\n')[1:]:  # Skip header
            line = line.strip()
            if line and not line.endswith(':'):
                # Split by comma if multiple skills on one line
                for skill in line.split(','):
                    skill = skill.strip()
                    if skill and len(skill) < 100:  # Reasonable length
                        skills.append(skill)
        
        return list(set(skills))[:30]  # Return unique, max 30 skills
    
    def _extract_experience(self) -> List[Dict[str, str]]:
        """Extract work experience and job titles"""
        experience = []
        
        try:
            experience_keywords = ['experience', 'work experience', 'professional experience']
            text_lower = self.raw_text.lower()
            
            # Find experience section
            exp_start = -1
            for keyword in experience_keywords:
                pos = text_lower.find(keyword)
                if pos != -1:
                    exp_start = pos
                    break
            
            if exp_start == -1:
                return experience
            
            # Find where experience section ends
            end_keywords = ['education', 'certification', 'skill', 'project']
            exp_end = len(self.raw_text)
            for keyword in end_keywords:
                pos = text_lower.find(keyword, exp_start + 20)
                if pos != -1 and pos < exp_end:
                    exp_end = pos
            
            exp_section = self.raw_text[exp_start:exp_end]
            
            # Parse experience entries (usually one per line or paragraph)
            for line in exp_section.split('\n')[1:]:
                line = line.strip()
                if line and any(char.isupper() for char in line):  # Has capitalized words (likely job title)
                    experience.append({
                        'title': line[:100],  # Truncate to reasonable length
                        'raw': line
                    })
            
            return experience[:10]  # Return max 10 positions
        except Exception as e:
            print(f"Error extracting experience: {e}")
            return experience
    
    def _extract_education(self) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        
        try:
            text_lower = self.raw_text.lower()
            edu_start = text_lower.find('education')
            
            if edu_start == -1:
                return education
            
            # Find where education section ends
            end_keywords = ['experience', 'certification', 'project', 'skill']
            edu_end = len(self.raw_text)
            for keyword in end_keywords:
                pos = text_lower.find(keyword, edu_start + 10)
                if pos != -1 and pos < edu_end:
                    edu_end = pos
            
            edu_section = self.raw_text[edu_start:edu_end]
            
            # Extract education entries
            for line in edu_section.split('\n')[1:]:
                line = line.strip()
                if line and len(line) > 5:
                    education.append({
                        'degree': line[:100],
                        'raw': line
                    })
            
            return education[:5]  # Return max 5 education entries
        except Exception as e:
            print(f"Error extracting education: {e}")
            return education
    
    def _extract_salary(self) -> str:
        """Extract salary expectations if mentioned"""
        keywords = ['salary', 'compensation', 'salary range', 'expected salary']
        text_lower = self.raw_text.lower()
        
        for keyword in keywords:
            pos = text_lower.find(keyword)
            if pos != -1:
                # Get the line containing salary info
                start = max(0, self.raw_text.rfind('\n', 0, pos))
                end = self.raw_text.find('\n', pos)
                if end == -1:
                    end = len(self.raw_text)
                
                salary_line = self.raw_text[start:end].strip()
                if len(salary_line) < 200:
                    return salary_line
        
        return ""
    
    def _extract_career_level(self) -> str:
        """Infer career level from resume content"""
        text_lower = self.raw_text.lower()
        
        # Check for level indicators
        if any(keyword in text_lower for keyword in ['ceo', 'director', 'vice president', 'vp', 'head of', 'leads']):
            return "senior/executive"
        elif any(keyword in text_lower for keyword in ['manager', 'lead', 'senior', 'principal']):
            return "mid-level/management"
        elif any(keyword in text_lower for keyword in ['junior', 'associate', 'analyst', 'intern']):
            return "junior/entry-level"
        else:
            return "mid-level"
    
    def get_resume_summary(self) -> str:
        """Get a formatted summary of the entire resume for LLM prompts"""
        if not self.resume_data:
            self.extract_resume()
        
        summary_parts = []
        
        # Professional Summary
        if self.resume_data.get('summary'):
            summary_parts.append(f"Professional Summary: {self.resume_data['summary']}")
        
        # Career Level
        if self.resume_data.get('career_level'):
            summary_parts.append(f"Career Level: {self.resume_data['career_level']}")
        
        # Skills
        if self.resume_data.get('skills'):
            skills_str = ", ".join(self.resume_data['skills'][:20])  # Top 20
            summary_parts.append(f"Top Skills: {skills_str}")
        
        # Experience
        if self.resume_data.get('experience'):
            exp_titles = [exp.get('title', '') for exp in self.resume_data['experience'][:5]]
            exp_str = " | ".join(exp_titles)
            summary_parts.append(f"Experience: {exp_str}")
        
        # Education
        if self.resume_data.get('education'):
            edu_str = " | ".join([edu.get('degree', '') for edu in self.resume_data['education'][:3]])
            summary_parts.append(f"Education: {edu_str}")
        
        # Salary
        if self.resume_data.get('salary_expectations'):
            summary_parts.append(f"Salary: {self.resume_data['salary_expectations']}")
        
        return "\n".join(summary_parts)
