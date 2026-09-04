from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from backend.app.schemas.common import ApiResponse
from backend.app.services.auth_service import AuthService
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=ApiResponse[TokenResponse], summary="Authenticate application user")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates an application user and returns a JWT access token.
    Pre-seeded demo credentials:
    - Admin: admin@crm.local / AdminPass123!
    - Sales Manager: manager@crm.local / ManagerPass123!
    - Sales Agent: agent@crm.local / AgentPass123!
    """
    service = AuthService(db)
    token_response = service.authenticate_user(login_data)
    return ApiResponse(data=token_response, message="Login successful.")

@router.get("/me", response_model=ApiResponse[UserResponse], summary="Retrieve current authenticated user profile")
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return ApiResponse(data=current_user)
