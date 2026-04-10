# Apify API connector
import requests
import json
import config

class ApifyConnector:
    def __init__(self):
        self.api_token = config.APIFY_API_TOKEN
        self.base_url = "https://api.apify.com/v2"
        self.timeout = config.APIFY_RUN_TIMEOUT  # 300 seconds max for sync endpoint

    def run_actor_sync(self, actor_id, input_data):
        """
        Run an Apify actor synchronously and get dataset items directly.
        This calls the run-sync-get-dataset-items endpoint.
        
        Args:
            actor_id: The actor ID or username~actor-name format
            input_data: The input payload for the actor
            
        Returns:
            A list of dataset items from the actor run
        """
        url = f"{self.base_url}/acts/{actor_id}/run-sync-get-dataset-items"
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"Running actor {actor_id} synchronously...")
            response = requests.post(
                url,
                json=input_data,
                headers=headers,
                timeout=self.timeout
            )
            
            # Handle different status codes
            if response.status_code == 201:
                print(f"Actor {actor_id} completed successfully")
                dataset_items = response.json()
                print(f"Retrieved {len(dataset_items)} items from actor {actor_id}")
                return dataset_items
            
            elif response.status_code == 408:
                error_data = response.json()
                raise TimeoutError(f"Actor run timed out: {error_data.get('error', {}).get('message', 'Unknown error')}")
            
            elif response.status_code == 400:
                error_data = response.json()
                raise RuntimeError(f"Actor run failed: {error_data.get('error', {}).get('message', 'Unknown error')}")
            
            elif response.status_code == 404:
                raise ValueError(f"Actor not found: {actor_id}")
            
            elif response.status_code == 429:
                raise RuntimeError("Rate limit exceeded. Please try again later.")
            
            else:
                raise RuntimeError(f"Unexpected response status {response.status_code}: {response.text}")
        
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request to actor {actor_id} timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling actor {actor_id}: {str(e)}")