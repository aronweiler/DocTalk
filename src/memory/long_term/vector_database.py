import os
import logging
import random

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

from models import User, Conversation


@contextmanager
def session_context(session):
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class VectorDatabase:
    def __init__(self):
        try:
            host = "localhost"
            port = int(os.environ.get("POSTGRES_PORT", 5432))
            database = os.environ.get("POSTGRES_DB", "postgres")
            user = os.environ.get("POSTGRES_USER", "postgres")
            password = os.environ.get("POSTGRES_PASSWORD", "postgres")

            engine = create_engine(
                f"postgresql://{user}:{password}@{host}:{port}/{database}"
            )

            # Create a cursor to execute SQL commands
            self.Session = sessionmaker(bind=engine)

        except (Exception, psycopg2.Error) as error:
            logging.error("Error while connecting to PostgreSQL", error)

    def find_user(self, session, name):
        return session.query(User).filter(User.name == name).first()

    def find_user_by_id(self, session, id):
        return session.query(User).filter(User.id == id).first()

    def update_user(self, session, user):
        existing_user = self.find_user(session, user.name)
        if existing_user is None:
            session.add(user)
        else:
            existing_user.age = user.age
            existing_user.location = user.location

    def delete_user_by_id(self, session, user_id):
        user = self.find_user_by_id(session, user_id)
        if user is not None:
            session.delete(user)

    def add_conversation(self, session, user, conversation):
        if user is not None:
            user.conversations.append(conversation)
        else:
            session.add(conversation)


if __name__ == "__main__":
    from dotenv import load_dotenv

    # Load environment variables from db.env
    if not load_dotenv("src/memory/long_term/db.env"):
        logging.error("Could not load environment variables from db.env")

    db = VectorDatabase()

    # Example: Create, add, and update a user
    with session_context(db.Session()) as s:
        user = User(name="John", age=25, location="New York")
        db.update_user(s, user)

        # Example: Query data from the table
        user = db.find_user(s, "John")
        print(f"Found: {user.name}")

        # Example: Update data in the table
        user.name = "Someone"

    # Example: Lookup, and delete a user
    with session_context(db.Session()) as s:
        user = db.find_user(s, "Someone")
        print(f"After update, found: {user.name}")

        # Example: Delete data from the table
        db.delete_user_by_id(s, user.id)

        user = db.find_user(s, "John Doe")

        if user is None:
            print("User not found")

    # Example: Add a conversation without a user association
    with session_context(db.Session()) as s:
        conversation = Conversation(
            message="Test Conversation",
            embedding=[random.random() for _ in range(1536)],
        )
        db.add_conversation(s, None, conversation)

        conversation = (
            s.query(Conversation)
            .filter(Conversation.message == "Test Conversation")
            .first()
        )
        print(f"Found: {conversation.message}, created: {conversation.record_created}")
