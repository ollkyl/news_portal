from fastapi import APIRouter, Request
from app import crud, schemas, state
from datetime import datetime, timezone
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
async def admin_panel(request: Request):
    return templates.TemplateResponse(
        "admin.html", {"request": request, "auto_update_enabled": state.auto_update_enabled}
    )


@router.post("/")
async def handle_admin_actions(request: Request):
    data = await request.json()

    if data.get("toggle_auto"):
        state.auto_update_enabled = not state.auto_update_enabled
        return {"status": "auto_update_toggled", "enabled": state.auto_update_enabled}

    elif data.get("title") and data.get("content"):
        news = schemas.NewsCreate(title=data["title"], content=data["content"])
        db_news = crud.create_news(news)
        state.latest_news_time = datetime.now(timezone.utc)

        for conn in crud.active_connections:
            await conn.send_json({"title": db_news.title, "content": db_news.content})
        return {"status": "news_added"}

    return {"status": "no_action"}
