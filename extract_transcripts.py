#!/usr/bin/env python3
"""
Main transcript extraction script
Extracts transcripts from Calendly and Fathom URLs
"""

import argparse
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

def sanitize_filename(name: str) -> str:
    """Sanitize filename for filesystem"""
    name = re.sub(r"[^a-zA-Z0-9.-]+", "-", name).strip("-")
    return name[:180] if len(name) > 180 else name

def extract_transcript_from_url(url: str, page, output_dir: Path):
    """Extract transcript from a single URL"""
    try:
        print(f"Extracting: {url[:60]}...")
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)  # Wait for content to load
        
        # Get page content
        content = page.evaluate("() => document.body.innerText")
        
        # Extract filename from URL
        if "calendly.com" in url:
            meeting_id = url.split("/")[-1]
            filename = f"calendly-{meeting_id}.txt"
        elif "fathom.video" in url:
            share_id = url.split("/")[-1]
            filename = f"fathom-{share_id}.txt"
        else:
            filename = sanitize_filename(url) + ".txt"
        
        output_path = output_dir / filename
        
        # Save transcript
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n\n")
            f.write(content)
        
        print(f"  ✓ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Extract transcripts from URLs")
    parser.add_argument("--urls", required=True, help="File containing URLs (one per line)")
    parser.add_argument("--output", default="transcripts/individual", help="Output directory")
    parser.add_argument("--headful", action="store_true", help="Run browser in visible mode")
    
    args = parser.parse_args()
    
    # Read URLs
    urls = []
    with open(args.urls, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not urls:
        print("No URLs found in file")
        return
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print(f"Extracting {len(urls)} transcripts")
    print("=" * 70)
    
    # Extract with Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headful)
        context = browser.new_context()
        page = context.new_page()
        
        success = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] ", end="")
            if extract_transcript_from_url(url, page, output_dir):
                success += 1
            else:
                failed += 1
            time.sleep(2)  # Be nice to servers
        
        browser.close()
    
    print("\n" + "=" * 70)
    print(f"Extraction complete!")
    print(f"  ✓ Success: {success}")
    print(f"  ✗ Failed: {failed}")
    print(f"\nFiles saved to: {output_dir}")

if __name__ == "__main__":
    main()

