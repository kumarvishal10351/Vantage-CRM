from typing import Optional
from sqlalchemy.orm import Session
from backend.app.repositories.user_repository import UserRepository
from backend.app.core.security import verify_password, create_access_token
from backend.app.core.exceptions import AuthenticationFailedException
from backend.app.schemas.auth import LoginRequest, TokenResponse, UserResponse

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def authenticate_user(self, login_data: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            raise AuthenticationFailedException("Invalid email or password.")

        if not verify_password(login_data.password, user.hashed_password):
            raise AuthenticationFailedException("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailedException("User account is deactivated.")

        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
        access_token = create_access_token(token_payload)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        return UserResponse.model_validate(user)
