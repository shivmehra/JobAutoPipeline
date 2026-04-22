#!/usr/bin/env python3
"""
Job Auto Pipeline - Main entry point
Uses synchronous Apify actor runs for simplified workflow
"""

import json
from src.apify_connector import ApifyConnector
from src.data_normalizer import DataNormalizer
from src.llm_filter import LLMFilter
from src.excel_writer import ExcelWriter
import config

def main():
    print("Starting Job Auto Pipeline (Synchronous Mode)...")

    # Initialize components
    apify = ApifyConnector()
    normalizer = DataNormalizer()
    normalizer.deduplicate()  # Remove duplicates before LLM filtering
    llm_filter = LLMFilter(model=config.OLLAMA_MODEL)
    excel_writer = ExcelWriter(
        config.EXCEL_FILE_PATH,
        config.EXCEL_SHEET_NAME
    )

    # Load resume from Word document for LLM-based filtering
    try:
        llm_filter.load_resume_document(config.FILTER_DOCUMENT_PATH)
        print("✓ Resume loaded for job matching")
    except Exception as e:
        print(f"✗ Error loading resume document: {e}")
        return

    # Run Apify actors synchronously and collect results
    print("\n" + "="*60)
    print("RUNNING ACTORS")
    print("="*60)
    
    all_actor_data = []
    
    for actor_name, actor_id in config.ACTOR_IDS.items():
        input_data = config.ACTOR_RUN_INPUTS.get(actor_name, {})
        print(f"\n➤ Running: {actor_name} ({actor_id})")
        
        try:
            # Run actor synchronously and get results immediately
            results = apify.run_actor_sync(actor_id, input_data)
            all_actor_data.append(results)
            print(f"✓ Successfully retrieved {len(results)} items")
            
        except TimeoutError as e:
            print(f"✗ TIMEOUT: {e}")
            # Continue with other actors even if one times out
            
        except Exception as e:
            print(f"✗ ERROR: {e}")
            # Continue with other actors even if one fails

    if not all_actor_data:
        print("\n✗ No data collected from any actors. Exiting.")
        return

    # Normalize data
    print("\n" + "="*60)
    print("DATA PROCESSING")
    print("="*60)
    
    print("\nNormalizing data...")
    normalized_data = normalizer.normalize_actor_data(all_actor_data, verbose=True)
    normalizer.save_to_json(config.NORMALIZED_DATA_PATH)
    print(f"✓ Normalized {len(normalized_data)} items")

    # Filter with LLM based on resume match
    print("\n" + "="*60)
    print("RESUME-BASED JOB FILTERING")
    print("="*60)
    print("\nScoring jobs against resume...")
    try:
        filtered_data = llm_filter.filter_items(normalized_data)
        if filtered_data:
            print(f"✓ {len(filtered_data)} jobs passed filtering (score ≥ 4)")
        else:
            print("⚠ No jobs passed filtering (score ≥ 4)")
    except Exception as e:
        print(f"✗ LLM filtering failed: {e}")
        print("Proceeding with unfiltered data...")
        filtered_data = normalized_data

    # Save to Excel with sorting and formatting
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    print("\nSaving results to Excel file...")
    try:
        success = excel_writer.write_data(filtered_data, sort_by_score=True)
        if success:
            print(f"✓ Results saved to {config.EXCEL_FILE_PATH}")
        else:
            print("✗ Error saving to Excel file")
    except Exception as e:
        print(f"✗ Error saving to Excel: {e}")

    print("\n" + "="*60)
    print("✓ PIPELINE COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
