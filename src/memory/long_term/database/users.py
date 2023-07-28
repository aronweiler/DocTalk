from typing import Union, List
from memory.long_term.models import User
from memory.long_term.database.vector_database import VectorDatabase


class Users(VectorDatabase):
    def __init__(self, db_env_location):
        super().__init__(db_env_location)

    # def find_user_by_name(self, name, eager_load: List[str]) -> Union[User, None]:
    #     query = session.query(User).filter(User.name == name)

    #     query = super().eager_load(query, eager_load)

    #     # If we have more than one user with this name, there's a problem
    #     if query.count() > 1:
    #         raise ValueError(f"More than one user with name {name} found.")

    #     return query.first()
        
    def find_user_by_email(self, session, email, eager_load = []) -> Union[User, None]:
        query = session.query(User).filter(User.email == email)

        query = super().eager_load(query, eager_load)

        return query.first()

    # def find_user_by_id(self, id, eager_load: List[str]) -> Union[User, None]:
    #     query = session.query(User).filter(User.id == id)

    #     query = super().eager_load(query, eager_load)

    #     return query.first()

    def add_update_user(self, session, user: User, eager_load) -> User:        
        query = session.query(User).filter(User.email == user.email)
        query = super().eager_load(query, eager_load)

        temp_user = query.first()

        if temp_user is not None:
            temp_user.name = user.name
            temp_user.age = user.age
            temp_user.location = user.location
            temp_user.email = user.email
            user = temp_user
        else:            
            session.add(user)

        return user

    def get_all_users(self, session, eager_load: List[str] = []) -> List[User]:
        query = session.query(User)

        query = super().eager_load(query, eager_load)

        return query.all()
