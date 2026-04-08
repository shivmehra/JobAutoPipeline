# Apify API connector
import os
from apify_client import ApifyClient
import config

class ApifyConnector:
    def __init__(self):
        self.client = ApifyClient(config.APIFY_API_TOKEN)

    def run_actor(self, actor_id, input_data):
        """Run an Apify actor and return the run ID"""
        run = self.client.actor(actor_id).call(run_input=input_data)
        return run['id']

    def get_run_results(self, run_id):
        """Get results from a completed actor run"""
        return self.client.run(run_id).dataset().iterate_items()