#!/usr/bin/env python3
"""
Setup script for Google Drive API
This will guide you through getting credentials
"""

import os
import json

print("=" * 70)
print("GOOGLE DRIVE API SETUP")
print("=" * 70)
print("\nTo upload files to Google Drive, you need to:")
print("\n1. Go to: https://console.cloud.google.com/")
print("2. Create a new project (or select an existing one)")
print("3. Enable the Google Drive API:")
print("   - Go to 'APIs & Services' > 'Library'")
print("   - Search for 'Google Drive API'")
print("   - Click 'Enable'")
print("\n4. Create OAuth credentials:")
print("   - Go to 'APIs & Services' > 'Credentials'")
print("   - Click 'Create Credentials' > 'OAuth client ID'")
print("   - If prompted, configure OAuth consent screen first")
print("   - Choose 'Desktop app' as application type")
print("   - Click 'Create'")
print("\n5. Download the credentials:")
print("   - Click the download icon next to your new OAuth client")
print("   - Save the JSON file")
print("\n6. Rename it to 'client_secrets.json'")
print("7. Place it in: /Users/isaacmarks/")
print("\n" + "=" * 70)
print("\nOnce you have the client_secrets.json file, run:")
print("  python3 upload_to_gdrive_simple.py")
print("\n" + "=" * 70)

# Check if file exists
if os.path.exists('/Users/isaacmarks/client_secrets.json'):
    print("\n✓ Found client_secrets.json!")
    print("You can now run: python3 upload_to_gdrive_simple.py")
else:
    print("\n✗ client_secrets.json not found")
    print("Please follow the steps above to create it.")

