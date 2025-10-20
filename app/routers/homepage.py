from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
from app import crud

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="", tags=["homepage"])


@router.get("/")
async def home(request: Request):
    news = crud.get_all_news()
    return templates.TemplateResponse("index.html", {"request": request, "news": news})
