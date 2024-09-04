from db import get_db
from db.models import User
from sqlalchemy.exc import IntegrityError


def check_user_exists(db, name=None, email=None, phone_number=None):
    query = db.query(User)
    if name:
        query = query.filter(User.name == name)
    if email:
        query = query.filter(User.email == email)
    if phone_number:
        query = query.filter(User.phone_number == phone_number)
    return query.first() is not None


def register_user_db(name, email, phone_number, password):
    with next(get_db()) as db:
        if check_user_exists(db, name=name):
            return 'Пользователь с таким именем уже существует'
        if check_user_exists(db, email=email):
            return 'Пользователь с таким email уже существует'
        if check_user_exists(db, phone_number=phone_number):
            return 'Пользователь с таким номером телефона уже существует'

        new_user = User(name=name, email=email, phone_number=phone_number, password=password)
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
            return 'Успешно зарегистрировались'
        except IntegrityError:
            db.rollback()
            return 'Ошибка при регистрации пользователя'

def get_all_users():
    with next(get_db()) as db:
        users = db.query(User).all()
        return users

def get_user_by_id(user_id):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        return user

def del_user_db(user_id):
    with next(get_db()) as db:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()



def change_user_db(user_id, change_info, new_info):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        if change_info == 'name':
            user.name = new_info
        elif change_info == 'email':
            user.email = new_info
        elif change_info == 'phone_number':
            user.phone_number = new_info
        elif change_info == 'password':
            user.password = new_info
        db.commit()
        db.refresh(user)
        return 'Успешно изменено'
    return 'Такого пользователя нету'


def get_user_by_name(name):
    with next(get_db()) as db:
        user = db.query(User).filter(User.name == name).first()
        return user

def get_user_by_email(email):
    with next(get_db()) as db:
        user = db.query(User).filter(User.email == email).first()
        return user

def get_user_by_phone(phone_number):
    with next(get_db()) as db:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        return user
