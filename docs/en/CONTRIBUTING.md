# Contributing Guide

## How to Contribute

1. Fork the repository
2. Create a branch for the new feature or fix
3. Make changes following the code standards
4. Create a pull request with a description of changes

## Code Standards

- Use Python 3.10 or newer
- Follow PEP 8
- Add types for new functions
- Update documentation when needed

## Project Structure

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
├── .gitignore
├── build.bat
├── run.bat
├── setup.bat
├── UPDATE.bat
└── requirements.txt
```

## Building the Project

1. Install dependencies:
```bash
setup.bat
```

2. Run for testing:
```bash
run.bat
```

3. Build exe file:
```bash
build.bat
```

## Testing

Test these operation modes:
- Single video download
- Multiple video download
- Playlist download
- Download in different formats
- MP3 conversion
- Auto-open folder
- Load/save URL lists
- Check all interface elements
- Check update system functionality
- Check progress display

## Update System Testing

When testing the update system, verify:
1. Update check at program start
2. Manual update through UPDATE.bat
3. Correct display of available updates
4. Update confirmation dialog
5. Successful file updates
6. Correct operation after update
7. Setup.bat execution after update if needed

## Creating a Release

1. Update version in files:
   - main.py (APP_VERSION)
   - docs/*/CHANGELOG.md
   - README files if needed

2. Test the full cycle:
   - Clean installation
   - Update process
   - All main features
   - Building exe file

3. Create release:
   - Create new tag in repository
   - Build final exe version
   - Create GitHub release
   - Add changelog and description
   - Upload compiled exe file

## Updating Documentation

When making changes, update:
1. Both README files (en/ru)
2. Documentation in docs/en and docs/ru
3. Add changelog entries
4. Update version numbers

## Reporting Issues

- Use GitHub Issues section
- Specify program version
- Describe steps to reproduce the error
- Attach error log from logs folder
- Include system information
- Screenshot if relevant

## Pull Request Process

1. Create branch with descriptive name
2. Update documentation if needed
3. Test all affected functionality
4. Create pull request with description:
   - What was changed
   - Why it was changed
   - How to test changes
   - Screenshots if UI changed