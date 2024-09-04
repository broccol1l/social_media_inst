from fastapi import APIRouter, HTTPException
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


@user_api.get("/check_name")
async def check_name(name: str):
    user = get_user_by_name(name)
    if user:
        raise HTTPException(status_code=400, detail="Имя уже занято")
    return {"message": "Имя доступно"}

@user_api.get("/check_email")
async def check_email(email: str):
    user = get_user_by_email(email)
    if user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return {"message": "Email доступен"}

@user_api.get("/check_phone")
async def check_phone(phone: str):
    user = get_user_by_phone(phone)
    if user:
        raise HTTPException(status_code=400, detail="Номер телефона уже зарегистрирован")
    return {"message": "Номер телефона доступен"}

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
    if not mail_validation:
        raise HTTPException(status_code=400, detail="Неправильный формат email")

    result = register_user_db(**user_data)
    if result != 'Успешно зарегистрировались':
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}