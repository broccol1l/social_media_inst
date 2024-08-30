from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Подключаем папку со статическими файлами
app.mount("/static", StaticFiles(directory="static"), name="static")

# Указываем папку с шаблонами
templates = Jinja2Templates(directory="api/templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})