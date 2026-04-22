# LLM filter using local Ollama with resume-based scoring
import os
import json
import re
from docx import Document
from ollama import Client
from src.resume_parser import ResumeParser

class LLMFilter:
    def __init__(self, model='mistral:7b'):
        self.client = Client(host='http://localhost:11434')
        self.model = model
        self.filter_criteria = ""  # Deprecated - kept for backward compatibility
        self.resume_data = {}
        self.resume_summary = ""

    def _extract_json_from_response(self, response_text):
        """
        Extract JSON object from response text that may contain extra text.
        LLM models often add explanations before/after the JSON object.
        """
        try:
            # Try direct parsing first (if response is pure JSON)
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON object if it's surrounded by text
        # Look for pattern: {...}
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        match = re.search(json_pattern, response_text)
        
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # If all else fails, return None
        return None

    def load_word_document(self, doc_path):
        """
        Load filter criteria from Word document (deprecated).
        Use load_resume_document() instead for resume-based filtering.
        """
        doc = Document(doc_path)
        self.filter_criteria = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.filter_criteria

    def load_resume_document(self, doc_path):
        """
        Load and parse resume from Word document for resume-based job filtering.
        Returns structured resume data.
        """
        try:
            parser = ResumeParser(doc_path)
            self.resume_data = parser.extract_resume()
            self.resume_summary = parser.get_resume_summary()
            print(f"✓ Resume loaded successfully")
            print(f"  Career Level: {self.resume_data.get('career_level', 'Unknown')}")
            print(f"  Skills: {len(self.resume_data.get('skills', []))} identified")
            return self.resume_data
        except Exception as e:
            print(f"✗ Error loading resume document: {e}")
            return None

    def score_job(self, item):
        """
        Use LLM to score how well a job matches the resume (1-10).
        Returns tuple: (score, rejection_reason)
        - score: int 1-10 (higher = better match)
        - rejection_reason: str or None (only for scores < 4)
        """
        if not self.resume_summary:
            print("WARNING: No resume loaded. Cannot score job.")
            return (5, None)  # Default to neutral score
        
        job_title = item.get('job_title', '')
        job_description = item.get('job_description', '')
        job_requirements = item.get('job_requirements', '')
        salary = item.get('salary_range', '')
        job_type = item.get('job_type', '')
        
        prompt = f"""You are a recruitment expert. Analyze how well this job matches the candidate's resume.

CANDIDATE RESUME:
{self.resume_summary}

JOB POSTING:
Title: {job_title}
Type: {job_type}
Salary Range: {salary}
Description: {job_description}
Requirements: {job_requirements}

Score this job match on a scale of 1-10 where:
- 10 = Perfect match (all skills, experience, and requirements align)
- 7-9 = Strong match (most requirements met)
- 4-6 = Moderate match (some relevant experience)
- 1-3 = Poor match (significant gaps or misalignment)

IMPORTANT: 
- Return ONLY a JSON object with exactly this format: {{"score": <number>, "reason": "<brief reason if score < 4, else null>"}}
- Score must be an integer 1-10
- If score >= 4, set reason to null
- If score < 4, provide a brief, specific reason (max 15 words)
- Do NOT include any text outside the JSON object"""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.1}  # Low temperature for consistent scoring
            )
            response_text = response['response'].strip()
            
            # Parse JSON response with fallback extraction
            try:
                result = self._extract_json_from_response(response_text)
                if result is None:
                    print(f"Warning: Could not extract JSON from response for job '{job_title[:30]}': {response_text[:100]}")
                    return (5, None)
                
                score = int(result.get('score', 5))
                reason = result.get('reason') if score < 4 else None
                
                # Validate score range
                score = max(1, min(10, score))
                
                return (score, reason)
            except (ValueError, TypeError, KeyError) as e:
                print(f"Warning: Invalid JSON data for job '{job_title[:30]}': {e}")
                return (5, None)  # Default to neutral
        except Exception as e:
            print(f"✗ Error scoring job '{job_title[:30]}': {e}")
            return (5, None)  # Default to neutral on error

    def filter_item(self, item):
        """
        Use LLM to determine if item matches filter criteria.
        Returns True if item should be kept, False otherwise.
        (Deprecated - use score_job() instead)
        """
        prompt = f"""
        Filter Criteria:
        {self.filter_criteria}

        Item to evaluate:
        Title: {item.get('title', '')}
        Description: {item.get('description', '')}
        URL: {item.get('url', '')}

        Based on the filter criteria above, should this item be included? Answer only with 'YES' or 'NO'.
        """

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.1}
            )
            answer = response['response'].strip().upper()
            
            if 'YES' in answer or answer.startswith('Y'):
                return True
            return False
        except Exception as e:
            print(f"Error filtering item: {e}")
            print(f"WARNING: Keeping item due to filter error: {item.get('title', 'Unknown')}")
            return True

    def filter_items(self, items):
        """
        Filter a list of job items using LLM scoring based on resume match.
        Keeps jobs with score >= 4.
        Returns filtered items with score and rejection_reason added.
        """
        if not self.resume_summary:
            print("WARNING: No resume loaded. Returning all items.")
            return items
        
        filtered_items = []
        rejected_count = 0
        total_score = 0
        
        print("\nScoring jobs against resume...")
        for i, item in enumerate(items, 1):
            score, reason = self.score_job(item)
            total_score += score
            
            # Add score and reason to item
            item['match_score'] = score
            item['rejection_reason'] = reason
            
            if score >= 4:
                filtered_items.append(item)
                print(f"  [{i}/{len(items)}] {item.get('job_title', 'Unknown')[:50]}... Score: {score} ✓")
            else:
                rejected_count += 1
                reason_str = f" - {reason}" if reason else ""
                print(f"  [{i}/{len(items)}] {item.get('job_title', 'Unknown')[:50]}... Score: {score} ✗{reason_str}")
        
        # Calculate and display statistics
        avg_score = total_score / len(items) if items else 0
        acceptance_rate = (len(filtered_items) / len(items) * 100) if items else 0
        
        print(f"\n{'='*60}")
        print(f"Filtering Summary:")
        print(f"  Total jobs: {len(items)}")
        print(f"  Kept (score ≥ 4): {len(filtered_items)}")
        print(f"  Rejected (score < 4): {rejected_count}")
        print(f"  Average score: {avg_score:.1f}/10")
        print(f"  Acceptance rate: {acceptance_rate:.1f}%")
        print(f"{'='*60}")
        
        return filtered_items