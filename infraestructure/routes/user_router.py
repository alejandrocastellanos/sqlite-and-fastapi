from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infraestructure.controllers.user_controller import UserController
from infraestructure.db.db import get_db
from infraestructure.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    instance_user_controller = UserController(db)
    new_user = instance_user_controller.new_user(user)
    return new_user

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    instance_user_controller = UserController(db)
    users_list = instance_user_controller.get_all_users()
    return users_list


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    instance_user_controller = UserController(db)
    user = instance_user_controller.get_user_by_id(user_id)
    return user
