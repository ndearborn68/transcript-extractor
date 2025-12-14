#!/usr/bin/env python3
"""
Prepare transcript files with proper client names
"""

import os
import re
from pathlib import Path
from shutil import copy2

def extract_client_name(file_path):
    """Extract client name from transcript file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    client_name = None
    date_str = None
    participant_info = None
    
    # Extract from content
    for i, line in enumerate(lines[:20]):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith('URL:'):
            continue
        
        # Extract date
        if re.match(r'[A-Za-z]+, [A-Za-z]+ \d+', line_stripped):
            date_str = line_stripped
            continue
        
        # Extract participant info
        if 'Isaac Marks and' in line_stripped:
            participant_info = line_stripped.replace('Isaac Marks and', '').strip()
            continue
        
        # Identify clients
        if 'Adelphi' in line_stripped or 'gguyan@adelphistaffing.com' in content:
            client_name = "Adelphi Staffing"
            break
        elif 'Leanne' in line_stripped or 'leanne.reilly@risustalent.com' in content:
            client_name = "Risu Talent - Leanne Reilly"
            break
        elif 'John W Frey' in content or ('John' in line_stripped and 'Frey' in content):
            client_name = "John W Frey - Healthcare Association"
            break
        elif 'Jeffrey A Davis' in content:
            client_name = "Jeffrey A Davis"
            break
        elif 'Jeff Hallam' in content or 'TLX Corp' in content:
            client_name = "TLX Corp - Jeff Hallam"
            break
        elif 'Enrique' in content and 'Rubio' in content:
            client_name = "Enrique Rubio - Latin America Talent"
            break
        elif 'Scott Mayo' in content:
            client_name = "Scott Mayo - Healthcare IT"
            break
        elif 'Joe' in line_stripped or 'jshanbaum@talentlineservices.com' in content:
            client_name = "TalentLine Services - Joe Shanbaum"
            break
        elif 'Sean Fitzmorris' in content:
            client_name = "Sean Fitzmorris"
            break
        elif 'Lori Clement' in content:
            client_name = "Lori Clement - Nonprofit Recruiting"
            break
        elif 'Doug Bryson' in content:
            client_name = "Doug Bryson"
            break
        elif 'Tom Vlach' in content:
            client_name = "Tom Vlach - Country Club Recruiting"
            break
        elif 'Garry Guyan' in content and 'locum' in content.lower():
            client_name = "Garry Guyan - Locum Tenens"
            break
        elif 'Steve McCarthy' in content or ('Kelly' in content and 'technology' in content.lower()):
            client_name = "Kelly Technology - Steve McCarthy"
            break
        elif 'Mark Nugent' in content:
            client_name = "Mark Nugent - Federal Placements"
            break
        elif 'John' in line_stripped and 'Westchester' in content:
            client_name = "John - Westchester Staffing"
            break
    
    # Fallback based on filename
    filename = Path(file_path).stem.lower()
    if not client_name:
        if 'adelphi' in filename:
            client_name = "Adelphi Staffing"
        elif 'leanne' in filename:
            client_name = "Risu Talent - Leanne Reilly"
        elif 'john' in filename and 'isaac' in filename:
            client_name = "John - Westchester Staffing"
        elif 'joe' in filename:
            client_name = "TalentLine Services - Joe Shanbaum"
        elif 'fathom' in filename:
            client_name = "Fathom Recording"
        else:
            # Try to extract from participant info
            if participant_info:
                # Clean email addresses
                participant_info = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', participant_info).strip()
                if participant_info:
                    client_name = f"Client - {participant_info}"
                else:
                    client_name = "Client Meeting"
            else:
                client_name = "Client Meeting"
    
    return client_name, date_str

def format_filename(client_name, date_str):
    """Format filename with client name and date"""
    # Clean client name for filename
    safe_name = re.sub(r'[^\w\s-]', '', client_name)
    safe_name = re.sub(r'\s+', '_', safe_name)
    
    # Extract date components if available
    date_part = ""
    if date_str:
        try:
            date_match = re.search(r'([A-Za-z]+), ([A-Za-z]+) (\d+)', date_str)
            if date_match:
                month_map = {
                    'January': '01', 'February': '02', 'March': '03', 'April': '04',
                    'May': '05', 'June': '06', 'July': '07', 'August': '08',
                    'September': '09', 'October': '10', 'November': '11', 'December': '12'
                }
                month = month_map.get(date_match.group(2), '')
                day = date_match.group(3).zfill(2)
                if month:
                    date_part = f"2024-{month}-{day}_"
        except:
            pass
    
    new_filename = f"{date_part}{safe_name}_Transcript.txt"
    return new_filename

def main():
    transcript_dir = Path('/Users/isaacmarks/transcripts/individual')
    output_dir = Path('/Users/isaacmarks/transcripts/ready_for_upload')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("Preparing Transcripts with Client Names")
    print("=" * 70)
    
    transcript_files = sorted(transcript_dir.glob('*.txt'))
    
    if not transcript_files:
        print(f"\nNo transcript files found in {transcript_dir}")
        return
    
    print(f"\nFound {len(transcript_files)} transcript files")
    print("=" * 70)
    
    prepared_files = []
    
    for file_path in transcript_files:
        try:
            client_name, date_str = extract_client_name(file_path)
            new_filename = format_filename(client_name, date_str)
            output_path = output_dir / new_filename
            
            # Copy file with new name
            copy2(file_path, output_path)
            
            print(f"\n{file_path.name}")
            print(f"  → {new_filename}")
            print(f"  Client: {client_name}")
            if date_str:
                print(f"  Date: {date_str}")
            
            prepared_files.append((new_filename, client_name))
            
        except Exception as e:
            print(f"\nError processing {file_path.name}: {e}")
    
    print("\n" + "=" * 70)
    print(f"✓ Prepared {len(prepared_files)} files")
    print(f"Location: {output_dir}")
    print("=" * 70)
    
    # Show summary by client
    print("\nFiles by Client:")
    client_groups = {}
    for filename, client in prepared_files:
        if client not in client_groups:
            client_groups[client] = []
        client_groups[client].append(filename)
    
    for client, files in sorted(client_groups.items()):
        print(f"\n{client}: {len(files)} file(s)")
        for f in files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()

