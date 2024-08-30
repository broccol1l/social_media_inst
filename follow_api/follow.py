from db.followservice import *
from fastapi import APIRouter

follow_router = APIRouter(prefix='/follow', tags=['Подписки'])



@follow_router.post('/add_follow')
async def add_follow_api(user_id: int, follow_id: int):
    return add_follow_db(user_id, follow_id)

@follow_router.delete('/delete_follow')
async def delete_follow_api(user_id: int, follow_id: int):
    return delete_follow_db(user_id, follow_id)

@follow_router.get('/get_follow_by_user_id')
async def get_follow_by_user_id_api(user_id: int):
    return get_all_follows_by_user_id_db(user_id)



