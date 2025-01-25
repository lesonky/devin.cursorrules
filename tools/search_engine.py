#!/usr/bin/env python3

import argparse
import sys
import time
import random
import os
import requests
import traceback
from typing import List, Dict
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

SERPER_API_KEY = os.getenv('SERPER_API_KEY')
SERPER_API_URL = 'https://google.serper.dev/search'

def get_random_user_agent() -> str:
    """
    Return a random User-Agent string to help prevent request blocking.
    
    Returns:
        str: A randomly selected user agent string
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)

def search_with_serper(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Perform search using Serper API.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict[str, str]]: List of search results with link, title, and snippet
        
    Raises:
        ValueError: If Serper API key is not found
        requests.exceptions.RequestException: If API request fails
    """
    if not SERPER_API_KEY:
        raise ValueError("Serper API key not found in environment variables")
        
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    data = {
        'q': query,
        'num': max_results
    }
    
    print(f"DEBUG: Searching with Serper API: {query}", file=sys.stderr)
    
    response = requests.post(SERPER_API_URL, headers=headers, json=data)
    response.raise_for_status()
    
    search_results = response.json()
    organic_results = search_results.get('organic', [])
    
    if not organic_results:
        print("DEBUG: No results found from Serper API", file=sys.stderr)
        return []
    
    results = []
    for result in organic_results:
        results.append({
            'href': result.get('link'),  # Changed to match format_results keys
            'title': result.get('title'),
            'body': result.get('snippet')  # Changed to match format_results keys
        })
    
    print(f"DEBUG: Found {len(results)} results from Serper API", file=sys.stderr)
    return results

def search_with_duckduckgo(query: str, max_results: int = 10, max_retries: int = 3, initial_delay: int = 2) -> List[Dict[str, str]]:
    """
    Perform search with DuckDuckGo as fallback.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        max_retries (int): Maximum number of retry attempts
        initial_delay (int): Initial delay between retries in seconds
        
    Returns:
        List[Dict[str, str]]: List of search results
        
    Raises:
        Exception: If all retry attempts fail
    """
    for attempt in range(max_retries):
        try:
            headers = {'User-Agent': get_random_user_agent()}
            
            print(f"DEBUG: DuckDuckGo Attempt {attempt + 1}/{max_retries} - Searching for query: {query}", 
                  file=sys.stderr)
            
            with DDGS(headers=headers) as ddgs:
                try:
                    results = list(ddgs.text(
                        query,
                        max_results=max_results,
                        backend='api'
                    ))
                except DuckDuckGoSearchException as api_error:
                    print(f"DEBUG: DuckDuckGo API backend failed, trying HTML backend: {str(api_error)}", 
                          file=sys.stderr)
                    time.sleep(1)
                    results = list(ddgs.text(
                        query,
                        max_results=max_results,
                        backend='html'
                    ))
                
                if not results:
                    print("DEBUG: No results found from DuckDuckGo", file=sys.stderr)
                    return []
                
                print(f"DEBUG: Found {len(results)} results from DuckDuckGo", file=sys.stderr)
                return results
                
        except Exception as e:
            print(f"ERROR: DuckDuckGo attempt {attempt + 1} failed: {str(e)}", file=sys.stderr)
            if attempt < max_retries - 1:
                delay = initial_delay * (attempt + 1) + random.random() * 2
                print(f"DEBUG: Waiting {delay:.2f} seconds before retry...", file=sys.stderr)
                time.sleep(delay)
            else:
                print("ERROR: All DuckDuckGo retry attempts failed", file=sys.stderr)
                raise

def format_results(results: List[Dict[str, str]]) -> None:
    """
    Format and print search results.
    
    Args:
        results (List[Dict[str, str]]): List of search results to format and print
    """
    for i, r in enumerate(results, 1):
        print(f"\n=== Result {i} ===")
        print(f"URL: {r.get('href', 'N/A')}")
        print(f"Title: {r.get('title', 'N/A')}")
        print(f"Snippet: {r.get('body', 'N/A')}")

def search(query: str, max_results: int = 10, max_retries: int = 3) -> None:
    """
    Main search function that tries Serper API first, then falls back to DuckDuckGo.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        max_retries (int): Maximum number of retry attempts
    """
    try:
        # Try Serper API first
        try:
            results = search_with_serper(query, max_results)
            if results:
                print("DEBUG: Using Serper API results", file=sys.stderr)
                format_results(results)
                return
        except Exception as serper_error:
            print(f"ERROR: Serper API search failed: {str(serper_error)}", file=sys.stderr)
            print("DEBUG: Falling back to DuckDuckGo", file=sys.stderr)
        
        # Fallback to DuckDuckGo
        results = search_with_duckduckgo(query, max_results)
        if results:
            print("DEBUG: Using DuckDuckGo results", file=sys.stderr)
            format_results(results)
            
    except Exception as e:
        print(f"ERROR: All search attempts failed: {str(e)}", file=sys.stderr)
        print(f"ERROR type: {type(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Search using Serper API with DuckDuckGo fallback")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10,
                      help="Maximum number of results (default: 10)")
    parser.add_argument("--max-retries", type=int, default=3,
                      help="Maximum number of retry attempts (default: 3)")
    
    args = parser.parse_args()
    search(args.query, args.max_results, args.max_retries)

if __name__ == "__main__":
    main()
