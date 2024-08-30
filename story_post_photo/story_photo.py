from fastapi import APIRouter, UploadFile, File
import random

story_photo_router = APIRouter(prefix='/photo', tags=['Фото для сториса'])

@story_photo_router.post('/add_story_photo')
async def add_photo_api(post_id: int, photo_file: UploadFile = File(...)):
    file_id = random.randint(1, 1000000)
    if photo_file:
        with open(f"db/story_photos/photo_{file_id}_{post_id}.txt", "wb") as photo:
            photo_to_save = await photo_file.read()
            photo.write(photo_to_save)
        return {'status': 1, "message": 'Сторис успешно загрузился'}
    return {'status': 0, 'message': 'Ошибка при загрузке'}