# Shared dependencies - dependencies.py
import httpx
from fastapi import Depends

# If you use any database or other services that require a connection or session,
# you would add them here as dependencies.

# Shared HTTP client for use in FastAPI dependency injection
async def get_http_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client

# Example usage in FastAPI route (in your FastAPI routes file)
# from dependencies import get_http_client

# @app.get('/some/path')
# async def some_route(client: httpx.AsyncClient = Depends(get_http_client)):
#     response = await client.get('https://example.com')
#     return response.json()