# Contributing Guide

## Development Environment Setup

### Initial Setup
1. Install Python 3.10 or newer
2. Clone the repository
3. Extract `RUS_BAT.zip` to the project root folder
   - BAT files are stored in archive to preserve correct Windows-1251 encoding
   - After extraction, you should have: setup.bat, run.bat, build.bat, UPDATE.bat
4. Run setup.bat to create virtual environment and install dependencies
5. Use run.bat to start the program
6. For creating exe, use build.bat

### Project Structure
```
jl-youtube-vk-downloader/
├── docs/
│   ├── en/
│   │   ├── CHANGELOG.md
│   │   ├── CONTRIBUTING.md
│   │   └── GUIDE.md
│   ├── img/
│   │   └── app.png
│   └── ru/
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       └── GUIDE.md
├── src/
│   ├── assets/
│   │   └── icon.ico
│   ├── downloader.py
│   ├── gui.py
│   └── main.py
├── build.bat              # From RUS_BAT.zip
├── run.bat               # From RUS_BAT.zip
├── setup.bat             # From RUS_BAT.zip
├── UPDATE.bat            # From RUS_BAT.zip
├── RUS_BAT.zip
├── .gitignore
├── requirements.txt
├── README.md
├── README_RU.md
└── LICENSE.md
```

## Code Standards
- Use Python 3.10 or newer
- Follow PEP 8
- Comment code in Russian
- Add types for new functions
- Update documentation when needed

## Testing
### Check Main Functions
- Single video download
- Multiple video download
- Playlist download
- Download in different formats
- MP3 conversion
- Auto-open folder
- Load/save URL lists
- All interface elements
- Update system
- Progress display

### Creating a Release
1. Update version in files:
   - main.py (APP_VERSION)
   - docs/*/CHANGELOG.md
   - README files if needed
2. Test:
   - Clean installation
   - Update process
   - Main features
   - Building exe file
3. Create release:
   - Create tag in repository
   - Build final exe version
   - Create GitHub release
   - Add changelog
   - Upload exe file and RUS_BAT.zip

## Updating Documentation
When making changes, update:
1. Both README files (en/ru)
2. Documentation in docs/en and docs/ru
3. Add changelog entries
4. Update version numbers

## Reporting Issues
- Use GitHub Issues section
- Specify program version
- Describe reproduction steps
- Attach error log from logs folder
- Include system information
- Add screenshot if needed

## Pull Request Process
1. Create branch with descriptive name
2. Update documentation if needed
3. Test changes
4. Create pull request with description:
   - What was changed
   - Why it was changed
   - How to test changes
   - Screenshots if UI changed