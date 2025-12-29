from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"