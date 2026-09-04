from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.user import AppUser

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[AppUser]:
        return self.db.query(AppUser).filter(AppUser.email == email.strip().lower()).first()

    def get_by_id(self, user_id: int) -> Optional[AppUser]:
        return self.db.query(AppUser).filter(AppUser.id == user_id).first()

    def create_user(self, email: str, hashed_password: str, full_name: str, role: str) -> AppUser:
        user = AppUser(
            email=email.strip().lower(),
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
