# CleanTrim

A simple script to organize files using consistent naming conventions. Useful for sorting photos from different devices, music albums, TV show episodes, and study materials such as textbooks, personal notes, classmates' notes, and professor's handouts. Ideal for keeping NAS libraries tidy and Jellyfin-compatible.

## Requirements

- Python 3 (standard library only, nothing to install)
- Windows (the optional log file uses Windows-style paths)

## Usage

1. **Back up your files first.** CleanTrim renames files for real.
2. Run the script:
   ```
   python CleanTrim.py
   ```
3. Paste the path of the folder to process (without quotes). Only the files directly inside the folder are renamed, subfolders are ignored.
4. Pick an action from the menu, check the preview, then confirm with `y` to write the new names.
