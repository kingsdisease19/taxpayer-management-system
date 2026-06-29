from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional, Tuple

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username (used for login)."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: dict) -> User:
        """Create a new user."""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update a user."""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """Hard delete a user."""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True

    def get_all(self, page: int = 1, limit: int = 20) -> Tuple[list, int]:
        """Get all users with pagination."""
        query = self.db.query(User)
        total = query.count()
        
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()
        
        return users, total