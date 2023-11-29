# schemas.py

from pydantic import BaseModel

class DecryptRequest(BaseModel):
    url: str
    mediaKey: str
    mimetype: str

class RunData(BaseModel):
    thread_id: str
    run_id: str