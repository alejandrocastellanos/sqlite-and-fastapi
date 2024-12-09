from fastapi import HTTPException
from sqlalchemy.orm import Session

from infraestructure.models.user import User
from infraestructure.schemas.user_schema import UserCreate


class UserController:

    def __init__(self, db: Session):
        self._db = db

    def new_user(self, user: UserCreate):
        db_user = User(name=user.name, age=user.age)
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def get_all_users(self):
        users = self._db.query(User).all()
        return users

    def get_user_by_id(self, user_id: int):
        db_user = self._db.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
