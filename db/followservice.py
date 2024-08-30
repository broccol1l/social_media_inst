from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db.models import Follow, User
from db import get_db  # Убедитесь, что у вас есть функция get_db для получения соединения


def add_follow_db(user_id, follow_id):
    with next(get_db()) as db:
        # Проверка, существуют ли пользователи
        user = db.query(User).filter(User.id == user_id).first()
        follow_user = db.query(User).filter(User.id == follow_id).first()

        if not user:
            return {'message': f'Пользователь с ID {user_id} не существует.'}
        if not follow_user:
            return {'message': f'Пользователь с ID {follow_id} не существует.'}

        # Проверка, не существует ли уже подписка
        existing_follow = db.query(Follow).filter_by(user_id=user_id, follow_id=follow_id).first()
        if existing_follow:
            return {'message': 'Подписка уже существует'}

        # Создание новой записи Follow
        new_follow = Follow(user_id=user_id, follow_id=follow_id)
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)

        return {
            'message': 'Подписка успешно добавлена',
            'follow': {
                'user_id': user_id,
                'user_name': user.name,
                'follow_id': follow_id,
                'follow_name': follow_user.name
            }
        }

def delete_follow_db(user_id, follow_id):
    with next(get_db()) as db:
        # Поиск записи Follow для удаления
        follow_to_delete = db.query(Follow).filter(
            Follow.user_id == user_id,
            Follow.follow_id == follow_id
        ).first()

        if not follow_to_delete:
            return {'message': 'Подписка не найдена'}

        db.delete(follow_to_delete)
        db.commit()

        return {
            'message': 'Подписка успешно удалена',
            'follow': {
                'user_id': user_id,
                'user_name': db.query(User).filter(User.id == user_id).first().name,
                'follow_id': follow_id,
                'follow_name': db.query(User).filter(User.id == follow_id).first().name
            }
        }

def get_all_follows_by_user_id_db(user_id):
    with next(get_db()) as db:
        # Получение всех записей Follow для данного user_id
        follows = db.query(Follow).filter(Follow.user_id == user_id).all()
        follow_list = []
        for follow in follows:
            follow_user = db.query(User).filter(User.id == follow.follow_id).first()
            follow_list.append({
                'follow_id': follow.follow_id,
                'follow_name': follow_user.name
            })
        return {
            'user_id': user_id,
            'follows': follow_list
        }

