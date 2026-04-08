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
                # Detect source based on unique fields or URL patterns
                if 'jobKey' in item:
                    source = 'Indeed'
                    item_id = item.get('jobKey', '')
                    title = item.get('title', '')
                    description = item.get('descriptionText', '')
                    url = item.get('jobUrl', '')
                    timestamp = item.get('datePublished', '')
                elif 'trackingId' in item:
                    source = 'LinkedIn'
                    item_id = item.get('id', '')
                    title = item.get('title', '')
                    description = item.get('descriptionText', '')
                    url = item.get('link', '')
                    timestamp = item.get('postedAt', '')
                elif 'jobId' in item and 'naukri' in item.get('url', '').lower():
                    source = 'Naukri'
                    item_id = item.get('jobId', '')
                    title = item.get('title', '')
                    description = item.get('description', item.get('shortDescription', ''))
                    url = item.get('url', '')
                    timestamp = item.get('createdDate', '')
                else:
                    # Fallback for unknown structures
                    source = 'unknown'
                    item_id = item.get('id', '')
                    title = item.get('title', item.get('name', ''))
                    description = item.get('description', '')
                    url = item.get('url', '')
                    timestamp = item.get('timestamp', '')

                # Create normalized item
                normalized_item = {
                    'id': item_id,
                    'title': title,
                    'description': description,
                    'url': url,
                    'source': source,
                    'timestamp': timestamp,
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