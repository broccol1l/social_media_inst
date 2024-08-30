from fastapi import APIRouter
from db.storypostservice import *

story_router = APIRouter(prefix='/stories', tags=['Сторисы'])



@story_router.post('/add_story')
async def add_story_api(user_id: int, main_text: str):
    post = add_story_post_db(user_id=user_id, text=main_text)
    if post:
        return 'Успешно добавлено'
    return False

@story_router.get('/get_story')
async def get_story(post_id):
    return get_all_or_exact_story_db(post_id)

@story_router.get('/get_all_stories')
async def get_all_stories():
    return get_all_stories_db()

@story_router.put('/change_story')
async def change_story_api(post_id: int, new_text: str):
    return change_story_text_db(post_id=post_id, text=new_text)

@story_router.delete('/delete_story')
async def delete_story_api(post_id: int):
    return delete_story_db(post_id)

#StoryLike
@story_router.post('/add_story_like')
async def add_story_like_api(story_id: int, user_id: int):
    return add_like_to_post_db(story_id, user_id)

@story_router.delete('/delete_story_like')
async def delete_story_like_api(story_id: int, user_id: int):
    return delete_like_from_post_db(story_id, user_id)

@story_router.get('/get_all_likes_by_post_id')
async def get_all_story_like_by_story_id(story_id: int):
    return get_all_likes_by_post_id_db(story_id)

@story_router.get('/get_all_stories_by_user_id')
async def get_all_stories_by_user_id(user_id: int):
    return get_all_likes_by_user_id_db(user_id)
