#!/usr/bin/env python3
"""
Job Auto Pipeline - Main entry point
"""

import time
import json
from src.apify_connector import ApifyConnector
from src.webhook_listener import run_webhook_server, get_webhook_data
from src.data_normalizer import DataNormalizer
from src.llm_filter import LLMFilter
from src.excel_writer import ExcelWriter
import config

def main():
    print("Starting Job Auto Pipeline...")

    # Initialize components
    apify = ApifyConnector()
    normalizer = DataNormalizer()
    llm_filter = LLMFilter(model=config.OLLAMA_MODEL)
    sheets_writer = ExcelWriter(
        config.EXCEL_FILE_PATH,
        config.EXCEL_SHEET_NAME
    )

    # Load filter criteria from Word document
    try:
        llm_filter.load_word_document(config.FILTER_DOCUMENT_PATH)
        print("Filter criteria loaded from Word document")
    except Exception as e:
        print(f"Error loading filter document: {e}")
        return

    # Start webhook server
    print(f"Starting webhook server on port {config.WEBHOOK_PORT}")
    webhook_thread = run_webhook_server(config.WEBHOOK_PORT)

    # Run Apify actors
    run_ids = []
    for actor_name, actor_id in config.ACTOR_IDS.items():
        print(f"Running actor: {actor_name} ({actor_id})")
        try:
            run_id = apify.run_actor(actor_id, {})  # Add input data as needed
            run_ids.append(run_id)
            print(f"Started run: {run_id}")
        except Exception as e:
            print(f"Error running actor {actor_name}: {e}")

    # Wait for webhook notifications
    print("Waiting for actor runs to complete...")
    completed_runs = set()
    all_actor_data = []

    while len(completed_runs) < len(run_ids):
        webhook_data = get_webhook_data()
        if webhook_data:
            run_id = webhook_data.get('resource', {}).get('id')
            if run_id and run_id not in completed_runs:
                print(f"Actor run completed: {run_id}")
                completed_runs.add(run_id)

                # Get results from completed run
                try:
                    results = list(apify.get_run_results(run_id))
                    all_actor_data.append(results)
                    print(f"Retrieved {len(results)} items from run {run_id}")
                except Exception as e:
                    print(f"Error getting results for run {run_id}: {e}")

        time.sleep(1)  # Check for webhooks every second

    # Normalize data
    print("Normalizing data...")
    normalized_data = normalizer.normalize_actor_data(all_actor_data)
    normalizer.save_to_json(config.NORMALIZED_DATA_PATH)
    print(f"Normalized {len(normalized_data)} items")

    # Filter with LLM
    print("Filtering data with LLM...")
    filtered_data = llm_filter.filter_items(normalized_data)
    print(f"Filtered to {len(filtered_data)} items")

    # Save to Excel File
    print("Saving results to Excel file...")
    success = sheets_writer.write_data(filtered_data)
    if success:
        print("Pipeline completed successfully!")
    else:
        print("Error saving to Excel file")

if __name__ == "__main__":
    main()
