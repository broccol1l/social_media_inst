from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, status

from api.user import user_api
from post_api.post import post_router
from photo_api.photo import photo_router
from friend_api.friend import friend_router
from story_post_api.story import story_router
from follow_api.follow import follow_router
from story_post_photo.story_photo import story_photo_router
from fastapi.templating import Jinja2Templates
from db import Base, engine



Base.metadata.create_all(engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_api)
app.include_router(post_router)
app.include_router(photo_router)
app.include_router(friend_router)
app.include_router(story_router)
app.include_router(story_photo_router)
app.include_router(follow_router)

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/main', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

