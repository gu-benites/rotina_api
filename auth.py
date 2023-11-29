import os
from datetime import datetime, timedelta
import json
import httpx
from fastapi import HTTPException

# Configuration Constants
HM_TOKEN_ENDPOINT = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
CREDENTIALS_DIR_PATH = os.environ.get("CREDENTIALS_DIR_PATH")
TOKEN_DIR_PATH = os.environ.get("TOKEN_DIR_PATH")

# Helper Functions
async def refresh_access_token(credentials, account_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': credentials['BASIC']
    }
    params = {
        'grant_type': 'client_credentials',
        'client_id': credentials['CLIENT_ID'],
        'client_secret': credentials['CLIENT_SECRET']
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(HM_TOKEN_ENDPOINT, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            expires_in = data['expires_in']
            expiration_date = datetime.now() + timedelta(seconds=expires_in)
            token_info = {
                'access_token': access_token,
                'expiration_date': expiration_date.isoformat()
            }

            # Save the token to a file
            token_file_path = os.path.join(TOKEN_DIR_PATH, f'hotmart_token_{account_name}.json')
            with open(token_file_path, 'w') as token_file:
                json.dump(token_info, token_file)
            return access_token
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to refresh access token")

def get_credentials(account_name: str):
    credentials_file_path = os.path.join(CREDENTIALS_DIR_PATH, f'hotmart_credentials_{account_name}.json')
    try:
        with open(credentials_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Credentials not found")

def is_token_expired(expiration_date_str):
    expiration_date = datetime.fromisoformat(expiration_date_str)
    return expiration_date <= datetime.now()