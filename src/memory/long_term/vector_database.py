import os
import logging
import random
from datetime import datetime

import openai

import psycopg2
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from contextlib import contextmanager

from memory.long_term.models import User, Conversation

from dotenv import load_dotenv

class VectorDatabase:
    def __init__(self, db_env_location):
        if not load_dotenv(db_env_location):
            raise ValueError("Could not load environment variables from db.env, memory will not work.")

        try:
            host = "localhost"
            port = int(os.environ.get("POSTGRES_PORT", 5432))
            database = os.environ.get("POSTGRES_DB", "postgres")
            user = os.environ.get("POSTGRES_USER", "postgres")
            password = os.environ.get("POSTGRES_PASSWORD", "postgres")

            engine = create_engine(
                f"postgresql://{user}:{password}@{host}:{port}/{database}"
            )

            self.Session = sessionmaker(bind=engine)

        except (Exception, psycopg2.Error) as error:
            raise ConnectionError("Error while connecting to PostgreSQL") from error

    @contextmanager
    def session_context(self, session):
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_user_by_name(self, session, name):
        return session.query(User).filter(User.name == name).first()

    def add_conversation(self, session, user_info, message, create_user_if_not_found = True, is_memory = False, additional_metadata = None):
        # try to find the user
        user = self.find_user_by_name(session, user_info["user_name"])

        # Create a new user if not found
        if user is None and create_user_if_not_found: 
            with self.session_context(session):
                user = User(name=user_info["user_name"], age=user_info["user_age"], location=user_info["user_location"])
                session.add(user)
                session.commit()

        # Create a vector from the text
        if user is not None:
            embedding = self._get_embedding(f"On {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}, User: {user.name} said: {message}")
        else:
            embedding = self._get_embedding(f"On {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}, message: {message}")
        
        conversation = Conversation(message=message, embedding=embedding, user_id=user.id, is_memory=is_memory, additional_metadata=additional_metadata)

        # if user is not None:
        #     user.conversations.append(conversation)
        # else:
        session.add(conversation)        

    def search_conversation_memory(self, session, query, top_k=5):
        # Not doing anything with user yet
        #user = self.find_user(session, user_name)

        # Create a vector from the text
        embedding = self._get_embedding(query)

        # Find the nearest neighbors
        nearest_neighbors = self.get_nearest_neighbors(session, embedding, top_k=top_k)

        # Return the nearest neighbors
        return nearest_neighbors

    def get_nearest_neighbors(self, session, embedding, top_k=5):    
        return session.scalars(select(Conversation).order_by(Conversation.embedding.l2_distance(embedding)).limit(top_k))    

    def _get_embedding(self, text, embedding_model="text-embedding-ada-002"):
        return openai.Embedding.create(input = [text], model=embedding_model)['data'][0]['embedding']

if __name__ == "__main__":
    from dotenv import load_dotenv

    db = VectorDatabase("src/memory/long_term/db.env")

    with db.session_context(db.Session()) as s:
        db.add_conversation(s, {"user_name": "John Doe", "user_age": 25, "user_location": "New York"}, "Hello, how are you?")

    with db.session_context(db.Session()) as s:
        conversations = db.search_conversation_memory(s, user_name="John Doe", query="Asking how I am")
        for conversation in conversations:
            print(f"Found: {conversation.message}")

    # Example: Create, add, and update a user
    with db.session_context(db.Session()) as s:
        user = User(name="John", age=25, location="New York")
        db.update_user(s, user)

        # Example: Query data from the table
        user = db.find_user(s, "John")
        print(f"Found: {user.name}")

        # Example: Update data in the table
        user.name = "Someone"

    # Example: Lookup, and delete a user
    with db.session_context(db.Session()) as s:
        user = db.find_user(s, "Someone")
        print(f"After update, found: {user.name}")

        # Example: Delete data from the table
        db.delete_user_by_id(s, user.id)

        user = db.find_user(s, "John Doe")

        if user is None:
            print("User not found")

    # Example: Add a conversation without a user association
    with db.session_context(db.Session()) as s:
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
