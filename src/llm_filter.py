# LLM filter using local Ollama
import os
import json
from docx import Document
from ollama import Client

class LLMFilter:
    def __init__(self, model='mistral:7b'):
        self.client = Client(host='http://localhost:11434')
        self.model = model
        self.filter_criteria = ""

    def load_word_document(self, doc_path):
        """Load filter criteria from Word document"""
        doc = Document(doc_path)
        self.filter_criteria = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.filter_criteria

    def filter_item(self, item):
        """
        Use LLM to determine if item matches filter criteria
        Returns True if item should be kept, False otherwise
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
                options={'temperature': 0.1}  # Low temperature for consistent filtering
            )
            answer = response['response'].strip().upper()
            
            # More robust response checking
            if 'YES' in answer or answer.startswith('Y'):
                return True
            return False
        except Exception as e:
            print(f"Error filtering item: {e}")
            # IMPORTANT: Return True on error to preserve data instead of deleting it
            print(f"WARNING: Keeping item due to filter error: {item.get('title', 'Unknown')}")
            return True

    def filter_items(self, items):
        """Filter a list of items using LLM"""
        if not self.filter_criteria:
            print("WARNING: No filter criteria loaded. Returning all items.")
            return items
        
        filtered_items = []
        for item in items:
            if self.filter_item(item):
                filtered_items.append(item)
        
        print(f"Filtered {len(items)} items → {len(filtered_items)} items kept")
        return filtered_items