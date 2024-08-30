from fastapi import APIRouter
from db.userservice import *
from pydantic import BaseModel
import re


regex = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")

def mail_checker(email):
    if re.fullmatch(regex, email):
        return True
    return False

user_api = APIRouter(prefix="/user", tags=["Пользователи"])



class User(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str


#Получение всех юзеров
@user_api.get("/all_user")
async def get_all_users_api():
    return get_all_users()

#Получение определенного юзера


@user_api.get("/get_exact_user")
async def get_exact_user(user_id):
    user = get_user_by_id(user_id)
    return user


#Удаление юзера
@user_api.delete("/delete_user")
async def delete_user_api(user_id):
    user_to_delete = del_user_db(user_id)
    return 'Пользователь удален'

@user_api.put('/update_user_data')
async def update_user_data(user_id: int, change_info: str, new_info: str):
    user = change_user_db(user_id, change_info, new_info)
    return user

@user_api.post("/add_user")
async def add_user_api(user_model: User):
    user_data = dict(user_model)
    mail_validation = mail_checker(user_model.email)
    if mail_validation:
        return register_user_db(**user_data)
    return "Неправильная email"