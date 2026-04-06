# Data normalizer for Apify actor results
import json

class DataNormalizer:
    def __init__(self):
        self.normalized_data = []

    def normalize_actor_data(self, actor_data_list):
        """
        Normalize data from multiple actors into a single JSON structure
        actor_data_list: list of data from different actors
        """
        normalized_items = []

        for actor_data in actor_data_list:
            for item in actor_data:
                # Normalize each item - this is a generic normalization
                # You may need to customize based on specific actor outputs
                normalized_item = {
                    'id': item.get('id', ''),
                    'title': item.get('title', item.get('name', '')),
                    'description': item.get('description', ''),
                    'url': item.get('url', ''),
                    'source': item.get('source', 'unknown'),
                    'timestamp': item.get('timestamp', ''),
                    'raw_data': item  # Keep original data
                }
                normalized_items.append(normalized_item)

        self.normalized_data = normalized_items
        return normalized_items

    def save_to_json(self, filename='normalized_data.json'):
        """Save normalized data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.normalized_data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filename='normalized_data.json'):
        """Load normalized data from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            self.normalized_data = json.load(f)
        return self.normalized_data