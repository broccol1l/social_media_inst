from sqlalchemy import func

from db import get_db
from db.models import UserPost, Comment, Hashtag, CommentLike, PostLike

# Добавление в бд пост
def add_user_post_db(user_id, text):
    with next(get_db()) as db:
        post = UserPost(user_id=user_id, main_text=text)
        db.add(post)
        db.commit()
        return True

#Получение всех постов или опред

def get_all_or_exact_post_db(post_id):
    with next(get_db()) as db:
        if post_id == 0:
            all_posts = db.query(UserPost).all()
            return all_posts
        else:
            post = db.query(UserPost).filter(UserPost.id == post_id).first()
            return post

def get_all_posts_db():
    with next(get_db()) as db:
        all_posts = db.query(UserPost).all()
        return all_posts

#Изменение поста

def change_post_text_db(post_id, text):
    with next(get_db()) as db:
        post = db.query(UserPost).filter(UserPost.id == post_id).first()
        if post:
            post.main_text = text
            db.commit()
            return 'Успешно изменено'
        return False

#Удаление поста

def delete_post_db(post_id):
    with next(get_db()) as db:
        delete_post = db.query(UserPost).filter_by(id=post_id)
        if delete_post:
            delete_post.delete()
            db.commit()
            return 'Успешно удалено'

#Добавление хэштега

def add_hashtag_db(name, post_id):
    with next(get_db()) as db:
        new_hashtag = Hashtag(hashtag_name=name, post_id=post_id)
        db.add(new_hashtag)
        db.commit()
        return 'Успешно добавлено'

#Получение хэштегов

def get_hashtag_db(name):
    with next(get_db()) as db:
        hashtag = db.query(Hashtag).filter_by(hashtag_name=name).all()
        return hashtag





def add_comment_db(user_id, post_id, text):
    with next(get_db()) as db:
        new_comment = Comment(user_id=user_id, post_id=post_id, text=text)
        db.add(new_comment)
        db.commit()
        return 'Успешно добавлено'


#Получение комментарий по пост айди

def get_comment_by_post_id(post_id):
    with next(get_db()) as db:
        comment_by_id = db.query(Comment).filter_by(post_id=post_id).all()
        return comment_by_id


def delete_comment_text(comment_id):
    with next(get_db()) as db:
        del_comment = db.query(Comment).filter_by(id=comment_id).first()
        return del_comment


# CommentLike

def add_like_comment_db(comment_id, user_id):
    with next(get_db()) as db:
        existing_like = db.query(CommentLike).filter_by(comment_id=comment_id, user_id=user_id).first()

        if existing_like:
            return {'message': 'Лайк уже существует'}

        new_like = CommentLike(comment_id=comment_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)

        # Считаем количество лайков для этого комментария
        like_count = db.query(func.count(CommentLike.id)).filter_by(comment_id=comment_id).scalar()

        return {
            'message': 'Лайк успешно добавлен',
            'comment_like': {
                'comment_id': new_like.comment_id,
                'user_id': new_like.user_id,
                'like_count': like_count
            }
        }

def delete_like_comment_db(comment_id, user_id):
    with next(get_db()) as db:
        delete_like = db.query(CommentLike).filter_by(comment_id=comment_id, user_id=user_id).first()
        if delete_like:
            db.delete(delete_like)
            db.commit()
            # Считаем количество лайков для этого комментария
            like_count = db.query(func.count(CommentLike.id)).filter_by(comment_id=comment_id).scalar()
            return {
                'message': 'Лайк успешно удален',
                'comment_like': {
                    'comment_id': comment_id,
                    'user_id': user_id,
                    'like_count': like_count
                }
            }
        return {'message': 'Лайк уже удален'}

def get_all_comment_like_by_comment_id_db(comment_id):
    with next(get_db()) as db:
        comment_likes = db.query(CommentLike).filter_by(comment_id=comment_id).all()
        like_count = len(comment_likes)
        return {
            'comment_id': comment_id,
            'like_count': like_count,
            'likes': [{'user_id': like.user_id} for like in comment_likes]
        }

def get_comment_like_by_user_id_db(user_id):
    with next(get_db()) as db:
        comment_likes = db.query(CommentLike).filter_by(user_id=user_id).all()
        return {
            'user_id': user_id,
            'likes': [{'comment_id': like.comment_id} for like in comment_likes]
        }

# PostLike

def add_like_post_db(post_id, user_id):
    with next(get_db()) as db:
        existing_like = db.query(PostLike).filter_by(post_id=post_id, user_id=user_id).first()

        if existing_like:
            return {'message': 'Лайк уже существует'}

        new_like = PostLike(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)

        # Считаем количество лайков для этого поста
        like_count = db.query(func.count(PostLike.id)).filter_by(post_id=post_id).scalar()

        return {
            'message': 'Лайк успешно добавлен',
            'post_like': {
                'post_id': post_id,
                'user_id': user_id,
                'like_count': like_count
            }
        }

def delete_like_post_db(post_id, user_id):
    with next(get_db()) as db:
        delete_like = db.query(PostLike).filter_by(post_id=post_id, user_id=user_id).first()
        if delete_like:
            db.delete(delete_like)
            db.commit()
            # Считаем количество лайков для этого поста
            like_count = db.query(func.count(PostLike.id)).filter_by(post_id=post_id).scalar()
            return {
                'message': 'Лайк успешно удален',
                'post_like': {
                    'post_id': post_id,
                    'user_id': user_id,
                    'like_count': like_count
                }
            }
        return {'message': 'Лайк уже удален'}

def get_post_like_by_user_id_db(user_id):
    with next(get_db()) as db:
        post_likes = db.query(PostLike).filter_by(user_id=user_id).all()
        return {
            'user_id': user_id,
            'likes': [{'post_id': like.post_id} for like in post_likes]
        }

def get_post_like_by_post_id_db(post_id):
    with next(get_db()) as db:
        post_likes = db.query(PostLike).filter_by(post_id=post_id).all()
        like_count = len(post_likes)
        return {
            'post_id': post_id,
            'like_count': like_count,
            'likes': [{'user_id': like.user_id} for like in post_likes]
        }
