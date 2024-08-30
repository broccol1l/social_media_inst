from datetime import datetime, timedelta

from db import get_db
from db.models import UserStoryPost, UserStoryLike, User


# Добавление в бд пост
def add_story_post_db(user_id, text):
    with next(get_db()) as db:
        post = UserStoryPost(user_id=user_id, main_text=text)
        db.add(post)
        db.commit()
        db.refresh(post)
        return {
            'message': 'Пост успешно добавлен',
            'post': {
                'id': post.id,
                'user_id': post.user_id,
                'main_text': post.main_text,
                'post_date': post.post_date.isoformat()  # Форматирование даты
            }
        }

def get_all_or_exact_story_db(post_id):
    with next(get_db()) as db:
        cutoff_time = datetime.now() - timedelta(days=1)
        if post_id == 0:
            recent_posts = db.query(UserStoryPost).filter(UserStoryPost.post_date >= cutoff_time).all()
            posts = []
            for post in recent_posts:
                user = db.query(User).filter(User.id == post.user_id).first()
                likes = db.query(UserStoryLike).filter(UserStoryLike.post_id == post.id).all()
                like_users = [db.query(User).filter(User.id == like.user_id).first().name for like in likes]
                posts.append({
                    'id': post.id,
                    'user_id': post.user_id,
                    'user_name': user.name if user else 'Unknown',
                    'main_text': post.main_text,
                    'post_date': post.post_date.isoformat(),
                    'likes': like_users
                })
            return {'posts': posts}
        else:
            post = db.query(UserStoryPost).filter(UserStoryPost.id == post_id).first()
            if post and post.post_date >= cutoff_time:
                user = db.query(User).filter(User.id == post.user_id).first()
                likes = db.query(UserStoryLike).filter(UserStoryLike.post_id == post.id).all()
                like_users = [db.query(User).filter(User.id == like.user_id).first().name for like in likes]
                return {
                    'post': {
                        'id': post.id,
                        'user_id': post.user_id,
                        'user_name': user.name if user else 'Unknown',
                        'main_text': post.main_text,
                        'post_date': post.post_date.isoformat(),
                        'likes': like_users
                    }
                }
            return {'message': 'Пост не найден или устарел'}

def get_all_stories_db():
    with next(get_db()) as db:
        # Определяем время 24 часа назад
        cutoff_time = datetime.now() - timedelta(days=1)
        recent_posts = db.query(UserStoryPost).filter(UserStoryPost.post_date >= cutoff_time).all()
        posts = []
        for post in recent_posts:
            user = db.query(User).filter(User.id == post.user_id).first()
            likes = db.query(UserStoryLike).filter(UserStoryLike.post_id == post.id).all()
            like_users = [db.query(User).filter(User.id == like.user_id).first().name for like in likes]
            posts.append({
                'id': post.id,
                'user_id': post.user_id,
                'user_name': user.name if user else 'Unknown',  # Имя пользователя
                'main_text': post.main_text,
                'post_date': post.post_date.isoformat(),
                'likes': like_users  # Список имен пользователей, которые поставили лайк
            })
        return {'posts': posts}

def change_story_text_db(post_id, text):
    with next(get_db()) as db:
        post = db.query(UserStoryPost).filter(UserStoryPost.id == post_id).first()
        if post:
            post.main_text = text
            db.commit()
            user = db.query(User).filter(User.id == post.user_id).first()
            return {
                'message': 'Текст поста успешно изменен',
                'post': {
                    'id': post.id,
                    'user_id': post.user_id,
                    'user_name': user.name if user else 'Unknown',
                    'main_text': post.main_text,
                    'post_date': post.post_date.isoformat()
                }
            }
        return {'message': 'Пост не найден'}

def delete_story_db(post_id):
    with next(get_db()) as db:
        cutoff_time = datetime.now() - timedelta(days=1)
        post_to_delete = db.query(UserStoryPost).filter_by(id=post_id).first()
        if post_to_delete and post_to_delete.post_date < cutoff_time:
            user = db.query(User).filter(User.id == post_to_delete.user_id).first()
            db.query(UserStoryLike).filter(UserStoryLike.post_id == post_id).delete()
            db.delete(post_to_delete)
            db.commit()
            return {
                'message': 'Пост успешно удален',
                'post': {
                    'id': post_to_delete.id,
                    'user_id': post_to_delete.user_id,
                    'user_name': user.name if user else 'Unknown',
                    'main_text': post_to_delete.main_text,
                    'post_date': post_to_delete.post_date.isoformat()
                }
            }
        return {'message': 'Пост не найден или не старше 24 часов'}


# StoryLike
def add_like_to_post_db(post_id, user_id):
    with next(get_db()) as db:
        # Проверка, существует ли лайк
        existing_like = db.query(UserStoryLike).filter_by(post_id=post_id, user_id=user_id).first()
        if existing_like:
            return {'message': 'Лайк уже существует'}

        # Создание нового лайка
        new_like = UserStoryLike(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {'message': 'Лайк успешно добавлен'}

# Удаление лайка из поста
def delete_like_from_post_db(post_id, user_id):
    with next(get_db()) as db:
        like_to_delete = db.query(UserStoryLike).filter_by(post_id=post_id, user_id=user_id).first()
        if like_to_delete:
            db.delete(like_to_delete)
            db.commit()
            return {'message': 'Лайк успешно удален'}
        return {'message': 'Лайк не найден'}

# Получение всех лайков для поста
def get_all_likes_by_post_id_db(post_id):
    with next(get_db()) as db:
        likes = db.query(UserStoryLike).filter_by(post_id=post_id).all()
        like_users = [db.query(User).filter(User.id == like.user_id).first().name for like in likes]
        return {
            'post_id': post_id,
            'likes': like_users
        }

# Получение всех лайков пользователя
def get_all_likes_by_user_id_db(user_id):
    with next(get_db()) as db:
        likes = db.query(UserStoryLike).filter_by(user_id=user_id).all()
        posts_liked = []
        for like in likes:
            post = db.query(UserStoryPost).filter(UserStoryPost.id == like.post_id).first()
            if post:
                posts_liked.append({
                    'post_id': post.id,
                    'post_text': post.main_text,
                    'post_date': post.post_date.isoformat()
                })
        return {
            'user_id': user_id,
            'liked_posts': posts_liked
        }

