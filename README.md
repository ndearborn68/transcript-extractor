# Transcript Extractor & Uploader

A Python toolset to extract transcripts from Fathom and Calendly meeting links and upload them to Google Drive with proper client labeling.

## Features

- ✅ Extract transcripts from Calendly meeting share links
- ✅ Extract transcripts from Fathom video share links  
- ✅ Automatically identify and label transcripts by client name
- ✅ Upload to Google Drive with organized naming
- ✅ Handle multiple transcripts in batch

## Requirements

- Python 3.9+
- Playwright (for browser automation)
- Google Drive API credentials (for upload)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd transcript-extractor
```

2. Install dependencies:
```bash
pip3 install playwright pydrive2
python3 -m playwright install chromium
```

3. Set up Google Drive API (for upload functionality):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Google Drive API
   - Create OAuth credentials (Desktop app)
   - Download and save as `client_secrets.json` in this directory

## Usage

### Step 1: Extract Transcripts

Create a file `urls.txt` with one URL per line:

```
https://calendly.com/s/meetings/abc123...
https://fathom.video/share/xyz789...
```

Run the extraction script:
```bash
python3 extract_transcripts.py --urls urls.txt --output transcripts/individual
```

Or use the Playwright-based extractor:
```bash
python3 extract_remaining_transcripts.py
```

### Step 2: Prepare Files with Client Names

Automatically label transcripts by client:
```bash
python3 prepare_transcripts_with_client_names.py
```

This will:
- Read all transcripts from `transcripts/individual/`
- Extract client names from content
- Create properly named files in `transcripts/ready_for_upload/`

### Step 3: Upload to Google Drive

**Option A: Manual Upload**
1. Open `transcripts/ready_for_upload/` folder
2. Drag files to your Google Drive folder

**Option B: Automated Upload**
1. Set up Google Drive API credentials (see Installation)
2. Update `FOLDER_ID` in `upload_transcripts_to_gdrive.py` with your Google Drive folder ID
3. Run:
```bash
python3 upload_transcripts_to_gdrive.py
```

## File Structure

```
transcript-extractor/
├── README.md
├── requirements.txt
├── extract_transcripts.py          # Main extraction script
├── extract_remaining_transcripts.py # Playwright-based extractor
├── prepare_transcripts_with_client_names.py  # Client labeling
├── upload_transcripts_to_gdrive.py  # Google Drive upload
├── quick_upload_gdrive.py          # Simplified upload script
├── setup_gdrive.py                 # Google Drive setup helper
├── transcripts/
│   ├── individual/                 # Raw extracted transcripts
│   └── ready_for_upload/          # Labeled transcripts ready for upload
└── .gitignore
```

## Configuration

### Google Drive Folder ID

To get your Google Drive folder ID:
1. Open the folder in Google Drive
2. Copy the ID from the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Update `FOLDER_ID` in the upload scripts

### Client Name Detection

The script automatically detects client names from:
- Meeting titles
- Participant email addresses
- Participant names in the transcript
- Filename patterns

You can customize client name extraction in `prepare_transcripts_with_client_names.py`.

## Examples

### Extract from Calendly URLs
```bash
python3 extract_remaining_transcripts.py
```

### Extract and prepare in one go
```bash
python3 extract_remaining_transcripts.py
python3 prepare_transcripts_with_client_names.py
```

### Upload to specific Google Drive folder
```python
# Edit upload_transcripts_to_gdrive.py
FOLDER_ID = "your-folder-id-here"
python3 upload_transcripts_to_gdrive.py
```

## Troubleshooting

### Playwright Issues
If Playwright fails to install:
```bash
python3 -m playwright install --force chromium
```

### Google Drive Authentication
If authentication fails:
1. Delete `mycreds.txt` and try again
2. Make sure `client_secrets.json` is in the project directory
3. Check that Google Drive API is enabled in your project

### Fathom Links Requiring Login
Some Fathom links may require authentication. The script will attempt extraction, but you may need to:
- Manually copy transcripts from Fathom
- Or use authenticated browser sessions

## Future Improvements

- [ ] Add support for other meeting platforms
- [ ] Automatic date extraction and sorting
- [ ] Duplicate detection
- [ ] Batch processing with progress tracking
- [ ] Export to different formats (PDF, DOCX)

## License

MIT License - feel free to use and modify for your needs.

## Contributing

Feel free to submit issues or pull requests for improvements!

