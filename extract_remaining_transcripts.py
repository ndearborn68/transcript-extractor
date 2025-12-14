#!/usr/bin/env python3
"""
Script to extract remaining Calendly and Fathom transcripts
Run this locally to extract the remaining transcripts
"""

import time
import os

# Remaining URLs to extract
remaining_urls = [
    ("calendly", "https://calendly.com/s/meetings/1c64fd60-7e39-4d20-9457-a22759cd7ea3"),
    ("calendly", "https://calendly.com/s/meetings/bfd68930-d07a-4e07-8aae-aa7329609862"),
    ("calendly", "https://calendly.com/s/meetings/85db87ec-8f59-4cd5-93c6-46e0b7c49542"),
    ("calendly", "https://calendly.com/s/meetings/6ac0384b-9046-46b0-a30c-fcca5ed7f09b"),
    ("calendly", "https://calendly.com/s/meetings/febace26-7b57-435c-b9dd-a4c2d3519313"),
    ("calendly", "https://calendly.com/s/meetings/acded289-1385-4c5a-8ee7-ebf68a2a3688"),
    ("fathom", "https://fathom.video/share/H2zezst6udSzRntms6UsFYN2er5Ff4fg"),
    ("fathom", "https://fathom.video/share/fN5ZXz2fggoTSqitzijq3BQaygDkV_qz"),
    ("fathom", "https://fathom.video/share/mVQwxJS_tpzXybNsrgkjns83dk7nT4kG"),
]

def extract_with_playwright():
    """Use Playwright to extract transcripts (recommended)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Install with: pip install playwright && playwright install chromium")
        return False
    
    output_dir = "/Users/isaacmarks/transcripts/individual"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        for i, (source, url) in enumerate(remaining_urls, start=12):
            try:
                print(f"Extracting {i}: {url}")
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Wait for content to load
                time.sleep(3)
                
                # Try to find transcript content
                # Calendly pages have the transcript in various places
                content = page.evaluate("""
                    () => {
                        // Try to get all text content
                        const body = document.body.innerText;
                        return body;
                    }
                """)
                
                # Extract just the transcript portion (after "Summary" or "Discussion")
                lines = content.split('\n')
                transcript_start = None
                for idx, line in enumerate(lines):
                    if 'Summary' in line or 'Discussion' in line or 'Action items' in line:
                        transcript_start = idx
                        break
                
                if transcript_start:
                    transcript = '\n'.join(lines[transcript_start:])
                else:
                    transcript = content
                
                # Save to file
                filename = f"{i:02d}-{source}-{url.split('/')[-1]}.txt"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n\n")
                    f.write(transcript)
                
                print(f"  ✓ Saved to {filename}")
                time.sleep(2)  # Be nice to the server
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
        browser.close()
    
    return True

if __name__ == "__main__":
    print("Extracting remaining transcripts...")
    print("=" * 60)
    
    if extract_with_playwright():
        print("\n✓ Extraction complete!")
        print(f"Files saved to: /Users/isaacmarks/transcripts/individual/")
    else:
        print("\nPlease install Playwright:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("\nThen run this script again.")

