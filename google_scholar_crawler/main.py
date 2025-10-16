#!/usr/bin/env python3
"""
Google Scholar Citation Data Crawler
Fetches citation information from Google Scholar and saves it as JSON files.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any

from scholarly import scholarly


def get_scholar_data(scholar_id: str) -> Dict[str, Any]:
    """
    Retrieve and process author data from Google Scholar.
    
    Args:
        scholar_id: Google Scholar ID to look up
        
    Returns:
        Dictionary containing author data with processed publications
    """
    # Fetch author data from Google Scholar
    author = scholarly.search_author_id(scholar_id)
    
    # Fill in detailed information about the author
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    
    # Add timestamp and convert publications to dictionary format
    author['updated'] = str(datetime.now())
    author['publications'] = {
        pub['author_pub_id']: pub for pub in author['publications']
    }
    
    return author


def save_scholar_data(author_data: Dict[str, Any], output_dir: str = 'results') -> None:
    """
    Save author data to JSON files.
    
    Args:
        author_data: Dictionary with author information
        output_dir: Directory where output files will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save complete author data
    with open(f'{output_dir}/gs_data.json', 'w') as outfile:
        json.dump(author_data, outfile, ensure_ascii=False)
    
    # Create and save shields.io compatible data
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author_data['citedby']}"
    }
    
    with open(f'{output_dir}/gs_data_shieldsio.json', 'w') as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)


def main():
    """Main function to fetch and save Google Scholar data."""
    try:
        # Get Google Scholar ID from environment variables
        scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID')
        if not scholar_id:
            raise ValueError("GOOGLE_SCHOLAR_ID environment variable not set")
        
        # Fetch and process author data
        author_data = get_scholar_data(scholar_id)
        
        # Print author data to console for debugging
        print(json.dumps(author_data, indent=2))
        
        # Save author data to output files
        save_scholar_data(author_data)
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()