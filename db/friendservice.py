from db import get_db
from db.models import Friend, User
from sqlalchemy.orm import joinedload

def add_friend_db(user_id, friend_id):
    with next(get_db()) as db:
        new_friend = Friend(user_id=user_id, friend_id=friend_id)
        if not new_friend:
            return 'Такого друга нету'

        if new_friend.user_id == new_friend.friend_id:
            return 'Нельзя добавить самого себя как друга'

        db.add(new_friend)
        db.commit()
        db.refresh(new_friend)
        return 'Друг успешно добавлен'

def delete_friend_db(user_id, friend_id):
    with next(get_db()) as db:
        delete_friend = db.query(Friend).filter_by(user_id=user_id, friend_id=friend_id)
        if delete_friend:
            delete_friend.delete()
            db.commit()
            return 'Друг успешно удален'
        return 'Такого друга нету'


# Получение всех друзей пользователя
def get_friend_by_user_id(user_id):
    with next(get_db()) as db:
        friends = db.query(Friend).options(joinedload(Friend.friend)).filter(Friend.user_id == user_id).all()
        return [
            {
                "friend_id": friend.friend_id,
                "name": friend.friend.name,
                "id": friend.id
            }
            for friend in friends
        ]

# Получение всех пользователей, у которых указан пользователь в друзьях
def get_users_by_friend_id(friend_id):
    with next(get_db()) as db:
        users = db.query(Friend).options(joinedload(Friend.user)).filter(Friend.friend_id == friend_id).all()
        return [
            {
                "user_id": user.user_id,
                "name": user.user.name,
                "id": user.id
            }
            for user in users
        ]



