#!/usr/bin/env python3
"""
Upload transcripts to Google Drive with proper client naming
"""

import os
import re
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import datetime

# Google Drive folder ID from the URL
FOLDER_ID = "1NbB4b0cOiHMw61HaVRnCGijRn2i6IfpO"

def extract_client_name(file_path):
    """Extract client name from transcript file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Try to find client name from various patterns
    client_name = None
    date_str = None
    
    # Pattern 1: Meeting title line (first non-empty line)
    for line in lines[:10]:
        line = line.strip()
        if not line or line.startswith('URL:'):
            continue
        
        # Skip common patterns
        if 'RecruitCloud' in line and 'meeting' in line.lower():
            continue
        if line.startswith('Summary') or line.startswith('Action items'):
            break
        
        # Extract date if present
        if re.match(r'[A-Za-z]+, [A-Za-z]+ \d+', line):
            date_str = line
            continue
        
        # Look for client indicators
        if ' - ' in line or ' and ' in line:
            # Extract client name
            if 'Adelphi' in line:
                client_name = "Adelphi Staffing"
                break
            elif 'Leanne' in line or 'risustalent.com' in content:
                client_name = "Risu Talent - Leanne Reilly"
                break
            elif 'John' in line and 'Frey' in content:
                client_name = "John W Frey - Healthcare Association"
                break
            elif 'Jeffrey A Davis' in content or 'Jeffrey' in line:
                client_name = "Jeffrey A Davis"
                break
            elif 'Jeff Hallam' in content or 'TLX Corp' in content:
                client_name = "TLX Corp - Jeff Hallam"
                break
            elif 'Enrique' in content:
                client_name = "Enrique Rubio - Latin America Talent"
                break
            elif 'Scott' in content and 'Mayo' in content:
                client_name = "Scott Mayo - Healthcare IT"
                break
            elif 'Joe' in line or 'jshanbaum@talentlineservices.com' in content:
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
            elif 'Steve McCarthy' in content or 'Kelly' in content:
                client_name = "Kelly Technology - Steve McCarthy"
                break
            elif 'Mark Nugent' in content:
                client_name = "Mark Nugent - Federal Placements"
                break
            elif 'John' in line and 'Westchester' in content:
                client_name = "John - Westchester Staffing"
                break
    
    # Extract date from content
    if not date_str:
        for line in lines[:15]:
            if re.match(r'[A-Za-z]+, [A-Za-z]+ \d+', line):
                date_str = line
                break
    
    # Fallback: use filename
    if not client_name:
        filename = Path(file_path).stem
        if 'adelphi' in filename.lower():
            client_name = "Adelphi Staffing"
        elif 'leanne' in filename.lower():
            client_name = "Risu Talent - Leanne Reilly"
        elif 'john' in filename.lower():
            client_name = "John"
        elif 'joe' in filename.lower():
            client_name = "TalentLine Services - Joe Shanbaum"
        elif 'fathom' in filename.lower():
            client_name = "Fathom Recording"
        else:
            client_name = "Client Meeting"
    
    return client_name, date_str

def format_filename(client_name, date_str, original_filename):
    """Format filename with client name and date"""
    # Clean client name for filename
    safe_name = re.sub(r'[^\w\s-]', '', client_name)
    safe_name = re.sub(r'\s+', '_', safe_name)
    
    # Extract date components if available
    date_part = ""
    if date_str:
        try:
            # Try to parse date (format: "Tuesday, November 25" or "Monday, November 24")
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
    
    # Create new filename
    new_filename = f"{date_part}{safe_name}_Transcript.txt"
    return new_filename

def main():
    transcript_dir = '/Users/isaacmarks/transcripts/individual'
    
    print("=" * 70)
    print("Upload Transcripts to Google Drive")
    print("=" * 70)
    
    # Check for client_secrets.json
    if not os.path.exists('/Users/isaacmarks/client_secrets.json'):
        print("\nERROR: client_secrets.json not found!")
        print("\nPlease run the setup script first:")
        print("  python3 setup_gdrive.py")
        print("\nOr manually create client_secrets.json by:")
        print("1. Going to https://console.cloud.google.com/")
        print("2. Creating OAuth credentials (Desktop app)")
        print("3. Downloading and saving as client_secrets.json")
        return
    
    # Authenticate
    print("\nAuthenticating with Google Drive...")
    print("(A browser window will open for authentication)")
    
    gauth = GoogleAuth()
    creds_file = "/Users/isaacmarks/mycreds.txt"
    
    if os.path.exists(creds_file):
        gauth.LoadCredentialsFile(creds_file)
    
    if gauth.credentials is None:
        print("\nFirst time setup - browser will open for authentication...")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    
    gauth.SaveCredentialsFile(creds_file)
    drive = GoogleDrive(gauth)
    
    # Verify folder access
    print(f"\nAccessing Google Drive folder: {FOLDER_ID}")
    try:
        folder = drive.CreateFile({'id': FOLDER_ID})
        folder.FetchMetadata()
        print(f"✓ Folder found: {folder['title']}")
    except Exception as e:
        print(f"✗ Error accessing folder: {e}")
        print("Please verify the folder ID and permissions.")
        return
    
    # Get all transcript files
    transcript_files = sorted(Path(transcript_dir).glob('*.txt'))
    
    if not transcript_files:
        print(f"\nNo transcript files found in {transcript_dir}")
        return
    
    print(f"\nFound {len(transcript_files)} transcript files")
    print("=" * 70)
    
    # Process and upload each file
    uploaded = []
    skipped = []
    errors = []
    
    for file_path in transcript_files:
        try:
            # Extract client name and date
            client_name, date_str = extract_client_name(file_path)
            new_filename = format_filename(client_name, date_str, file_path.name)
            
            print(f"\nProcessing: {file_path.name}")
            print(f"  Client: {client_name}")
            print(f"  New filename: {new_filename}")
            
            # Check if file already exists
            existing_files = drive.ListFile({
                'q': f"title='{new_filename}' and '{FOLDER_ID}' in parents and trashed=false"
            }).GetList()
            
            if existing_files:
                print(f"  ⊘ Already exists, skipping")
                skipped.append(new_filename)
            else:
                # Upload file
                print(f"  Uploading...", end=' ', flush=True)
                file_drive = drive.CreateFile({
                    'title': new_filename,
                    'parents': [{'id': FOLDER_ID}]
                })
                file_drive.SetContentFile(str(file_path))
                file_drive.Upload()
                print("✓")
                uploaded.append(new_filename)
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")
            errors.append((file_path.name, str(e)))
    
    # Summary
    print("\n" + "=" * 70)
    print("Upload Summary:")
    print("=" * 70)
    print(f"  ✓ Uploaded: {len(uploaded)} files")
    print(f"  ⊘ Skipped (already exist): {len(skipped)} files")
    if errors:
        print(f"  ✗ Errors: {len(errors)} files")
        for filename, error in errors:
            print(f"    - {filename}: {error[:50]}")
    
    print(f"\nFolder: {folder['title']}")
    print(f"View folder: https://drive.google.com/drive/folders/{FOLDER_ID}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Installing required package: pydrive2")
        os.system("pip3 install pydrive2")
        print("\nPlease run the script again:")
        print("  python3 upload_transcripts_to_gdrive.py")

