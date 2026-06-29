from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

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

    # Username must be unique and is required for each user
    username = Column(String, unique=True, index=True, nullable=False)

    # Email address must be unique and is required
    email = Column(String, unique=True, index=True, nullable=False)

    # Stored password hash for authentication
    password_hash = Column(String, nullable=False)

    # Role of the user in the application
    role = Column(String, nullable=False, default="registration_officer")

    # Indicates whether the user account is active
    is_active = Column(Boolean, default=True)

    # Timestamp when the user was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp when the user was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())