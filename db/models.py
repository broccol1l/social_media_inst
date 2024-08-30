from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

# User,Userpost, postphoto, comment, hashtag, follow, friend, commentlike, postlike, userstorypost


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, )
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(DateTime, default=datetime.now())

class UserPost(Base):
    __tablename__ = 'user_posts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    main_text = Column(String, nullable=False)
    post_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user_fk = relationship(User, lazy='subquery')

class PostPhoto(Base):
    __tablename__ = 'photos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    post_id = Column(Integer, ForeignKey('user_posts.id'))
    photo = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now())

    post_fk = relationship(UserPost, lazy='subquery')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('user_posts.id'))
    date = Column(DateTime, default=datetime.now())

    user_fk = relationship(User, lazy='subquery')
    post_fk = relationship(UserPost, lazy='subquery')

class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hashtag_name = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('user_posts.id'))
    date = Column(DateTime, default=datetime.now())

    post_fk = relationship(UserPost, lazy='subquery')


class Friend(Base):
    __tablename__ = 'friends'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    user = relationship('User', foreign_keys=[user_id])
    friend = relationship('User', foreign_keys=[friend_id])
class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    follow_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', foreign_keys=[user_id], lazy='subquery')
    follow = relationship('User', foreign_keys=[follow_id], lazy='subquery')

class CommentLike(Base):
    __tablename__ = 'comment_likes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))

    user_fk = relationship(User, lazy='subquery')
    comment_fk = relationship(Comment, lazy='subquery')


class PostLike(Base):
    __tablename__ = 'post_likes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('user_posts.id'))

    user_fk = relationship(User, lazy='subquery')
    post_fk = relationship(UserPost, lazy='subquery')

class UserStoryPost(Base):
    __tablename__ = 'user_story_posts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    main_text = Column(String, nullable=False)
    post_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user_fk = relationship(User, lazy='subquery')

class UserStoryPhoto(Base):
    __tablename__ = 'story_photos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    post_id = Column(Integer, ForeignKey('user_story_posts.id'))
    photo = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now())

    post_fk = relationship(UserStoryPost, lazy='subquery')


class UserStoryLike(Base):
    __tablename__ = 'user_story_likes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('user_story_posts.id'))

    user_fk = relationship(User, lazy='subquery')
    post_fk = relationship(UserStoryPost, lazy='subquery')



