from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    CheckConstraint,
)
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    location = Column(String, nullable=True)

    # Define a one-to-many relationship with Conversation
    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    record_created = Column(DateTime, nullable=False, default=datetime.now)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    additional_metadata = Column(String, nullable=True)
    embedding = Column(Vector(1536), nullable=True)

    # Define the ForeignKeyConstraint to ensure the user_id exists in the users table
    user_constraint = ForeignKeyConstraint([user_id], [User.id])

    # Define the CheckConstraint to enforce user_id being NULL or existing in users table
    user_check_constraint = CheckConstraint(
        "user_id IS NULL OR user_id IN (SELECT id FROM users)",
        name="ck_user_id_in_users",
    )

    # Define the relationship with User
    user = relationship("User", back_populates="conversations")
