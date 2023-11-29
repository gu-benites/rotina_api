# config.py

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Use environment variables or default values if not set
CREDENTIALS_DIR_PATH = Path(os.environ.get("CREDENTIALS_DIR_PATH"))
TOKEN_DIR_PATH = Path(os.environ.get("TOKEN_DIR_PATH"))
AUDIO_FILES_DIR = Path(os.environ.get("AUDIO_FILES_DIR"))

HM_TOKEN_ENDPOINT = 'https://api-sec-vlc.hotmart.com/security/oauth/token'

# OpenAI settings
OPENAI_ORG_ID = os.environ.get("OPENAI_ORG_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_EMBED = os.environ.get("OPENAI_MODEL_EMBED")

# Pinecone settings
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_REGION = os.environ.get("PINECONE_REGION")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")

# Selenium Chrome Driver Path
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")

# Directories Creation
def create_directories():
    for directory in [CREDENTIALS_DIR_PATH, TOKEN_DIR_PATH, AUDIO_FILES_DIR]:
        if not directory.exists():
            directory.mkdir(parents=True)

# Call the directory creation function
create_directories()