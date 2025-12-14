# Quick Start Guide

## One-Time Setup

1. **Install dependencies:**
```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

2. **Set up Google Drive (optional, for automated upload):**
```bash
python3 setup_gdrive.py
# Follow instructions to get client_secrets.json
```

## Usage Workflow

### Step 1: Extract Transcripts

Create `urls.txt` with your meeting URLs:
```
https://calendly.com/s/meetings/abc123...
https://fathom.video/share/xyz789...
```

Run extraction:
```bash
python3 extract_transcripts.py --urls urls.txt --output transcripts/individual
```

Or use the Playwright extractor (handles JS-heavy pages better):
```bash
# Edit extract_remaining_transcripts.py to add your URLs
python3 extract_remaining_transcripts.py
```

### Step 2: Label by Client

Automatically identify and label clients:
```bash
python3 prepare_transcripts_with_client_names.py
```

Files will be in `transcripts/ready_for_upload/` with client names.

### Step 3: Upload to Google Drive

**Manual (easiest):**
- Open `transcripts/ready_for_upload/` folder
- Drag files to Google Drive

**Automated:**
1. Edit `upload_transcripts_to_gdrive.py` - set your `FOLDER_ID`
2. Run: `python3 upload_transcripts_to_gdrive.py`

## Repository

**GitHub:** https://github.com/ndearborn68/transcript-extractor

## Need Help?

See README.md for detailed documentation and troubleshooting.

