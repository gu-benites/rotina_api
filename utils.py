# Utility functions - utils.py
import os
from datetime import datetime, timedelta
from pathlib import Path

# Path constants
AUDIO_FILES_DIR = Path(os.environ.get("AUDIO_FILES_DIR"))

# Utility function that cleans up old audio files
async def cleanup_audio_files():
    for file_name in os.listdir(AUDIO_FILES_DIR):
        file_path = os.path.join(AUDIO_FILES_DIR, file_name)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if datetime.now() - creation_time > timedelta(days=1):  # Adjust the cleanup threshold as needed
            os.remove(file_path)

# You can add additional utility functions as needed here. These might include:
# - Functions to validate input data.
# - Date and time conversion functions.
# - Functions to format messages or data for output.
# - Other miscellaneous functions that are used in multiple places across your application.
