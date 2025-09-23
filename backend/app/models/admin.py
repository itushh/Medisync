from pydantic import BaseModel

class AdminLogin(BaseModel):
    email: str
    key: str

class Token(BaseModel):
    access_token: str
    token_type: str
