from fastapi import APIRouter
from db.friendservice import *

friend_router = APIRouter(prefix='/friend', tags=['Друзья'])




@friend_router.post('/add_friend')
async def add_friend_api(user_id: int, friend_id: int):
    return add_friend_db(user_id, friend_id)

@friend_router.delete('/delete_friend')
async def delete_friend_api(user_id: int, friend_id: int):
    return delete_friend_db(user_id, friend_id)

@friend_router.get('/get_friend_by_user_id')
async def get_friend_by_user_id_api(user_id: int):
    return get_friend_by_user_id(user_id)

@friend_router.get('/get_users_by_friend_id')
async def get_users_by_friend_id_api(friend_id: int):
    return get_users_by_friend_id(friend_id)

