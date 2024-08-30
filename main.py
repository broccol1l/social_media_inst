from fastapi import FastAPI

from api.user import user_api
from post_api.post import post_router
from photo_api.photo import photo_router
from friend_api.friend import friend_router
from story_post_api.story import story_router
from follow_api.follow import follow_router
from story_post_photo.story_photo import story_photo_router
from db import Base, engine



Base.metadata.create_all(engine)

app = FastAPI(docs_url="/")

app.include_router(user_api)
app.include_router(post_router)
app.include_router(photo_router)
app.include_router(friend_router)
app.include_router(story_router)
app.include_router(story_photo_router)
app.include_router(follow_router)