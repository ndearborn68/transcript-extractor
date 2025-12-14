#!/usr/bin/env python3
"""
Quick upload to Google Drive using folder ID
This script will guide you through OAuth setup if needed
"""

import os
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

FOLDER_ID = "1NbB4b0cOiHMw61HaVRnCGijRn2i6IfpO"

def main():
    upload_dir = Path('/Users/isaacmarks/transcripts/ready_for_upload')
    
    print("=" * 70)
    print("Upload Transcripts to Google Drive")
    print("=" * 70)
    
    # Check for credentials
    if not os.path.exists('/Users/isaacmarks/client_secrets.json'):
        print("\n" + "=" * 70)
        print("SETUP REQUIRED - One-time OAuth Setup")
        print("=" * 70)
        print("\nTo upload files, you need to authenticate with Google Drive.")
        print("This is a one-time setup process:\n")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a project (or select existing)")
        print("3. Enable 'Google Drive API'")
        print("4. Go to 'Credentials' > 'Create Credentials' > 'OAuth client ID'")
        print("5. Choose 'Desktop app'")
        print("6. Download the JSON file")
        print("7. Save it as: /Users/isaacmarks/client_secrets.json")
        print("\n" + "=" * 70)
        print("\nAlternatively, you can manually upload the files:")
        print(f"  Location: {upload_dir}")
        print(f"  Google Drive folder: https://drive.google.com/drive/folders/{FOLDER_ID}")
        print("\n" + "=" * 70)
        return
    
    # Authenticate
    print("\nAuthenticating...")
    gauth = GoogleAuth()
    creds_file = "/Users/isaacmarks/mycreds.txt"
    
    if os.path.exists(creds_file):
        gauth.LoadCredentialsFile(creds_file)
    
    if gauth.credentials is None:
        print("\nOpening browser for authentication...")
        print("Please sign in and grant permissions.")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    
    gauth.SaveCredentialsFile(creds_file)
    drive = GoogleDrive(gauth)
    
    # Verify folder
    print(f"\nAccessing folder: {FOLDER_ID}")
    try:
        folder = drive.CreateFile({'id': FOLDER_ID})
        folder.FetchMetadata()
        print(f"✓ Folder: {folder['title']}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Get files to upload
    files = sorted(upload_dir.glob('*.txt'))
    if not files:
        print(f"\nNo files found in {upload_dir}")
        return
    
    print(f"\nFound {len(files)} files to upload")
    print("=" * 70)
    
    uploaded = []
    skipped = []
    errors = []
    
    for file_path in files:
        filename = file_path.name
        try:
            print(f"Uploading: {filename[:60]}...", end=' ', flush=True)
            
            # Check if exists
            existing = drive.ListFile({
                'q': f"title='{filename}' and '{FOLDER_ID}' in parents and trashed=false"
            }).GetList()
            
            if existing:
                print("(exists)")
                skipped.append(filename)
            else:
                file_drive = drive.CreateFile({
                    'title': filename,
                    'parents': [{'id': FOLDER_ID}]
                })
                file_drive.SetContentFile(str(file_path))
                file_drive.Upload()
                print("✓")
                uploaded.append(filename)
        except Exception as e:
            print(f"✗ {str(e)[:50]}")
            errors.append((filename, str(e)))
    
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  ✓ Uploaded: {len(uploaded)}")
    print(f"  ⊘ Skipped: {len(skipped)}")
    if errors:
        print(f"  ✗ Errors: {len(errors)}")
    print(f"\nView folder: https://drive.google.com/drive/folders/{FOLDER_ID}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Installing pydrive2...")
        os.system("pip3 install pydrive2")
        print("\nRun again: python3 quick_upload_gdrive.py")

