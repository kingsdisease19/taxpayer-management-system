import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.base import Base


class RoleEnum(str, enum.Enum):
    REGISTRATION_OFFICER = "registration_officer"
    SUPERVISOR = "supervisor"
    ADMINISTRATOR = "administrator"

# User model for the database.
# This model maps to the `users` table and defines the columns used to store user data.
# Fields:
# - id: primary key for the user record
# - username: unique username for login or identification
# - email: unique email address for the user
# - password_hash: hashed password value for authentication
# - role: user role within the system, defaults to registration officer
# - is_active: flag indicating whether the user account is active
# - created_at: timestamp when the user record was created
# - updated_at: timestamp when the user record was last updated
class User(Base):
    __tablename__ = "users"

    # Primary key for the user table
    id = Column(Integer, primary_key=True, index=True)

    # Unique username for the user, used for login or identification
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    email = Column(String(120), unique=True, index=True, nullable=False)
    
    # Hashed password for the user, stored securely
    password_hash = Column(String(255), nullable=False)  # bcrypt hashes are ~60 chars

    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.REGISTRATION_OFFICER)

    # Indicates whether the user account is active
    is_active = Column(Boolean, default=True)

    # Timestamp when the user was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp when the user was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())