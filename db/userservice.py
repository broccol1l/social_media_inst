from db import get_db
from db.models import User

def register_user_db(name, email, phone_number, password):
    with next(get_db()) as db:
        new_user = User(name=name, email=email, phone_number=phone_number, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return 'Успешно зарегистрировались'

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

