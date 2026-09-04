from pydantic import BaseModel, Field, ConfigDict

class LoginRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "admin@crm.local"})
    password: str = Field(..., json_schema_extra={"example": "AdminPass123!"})

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
