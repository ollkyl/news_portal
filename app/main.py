from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import asyncio
from datetime import datetime, timezone

from app.db import Base, engine
from app import crud, schemas
from app.parser import get_latest_news

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

Base.metadata.create_all(bind=engine)

auto_update_enabled = False
latest_news_time = datetime.now(timezone.utc)


@app.get("/")
async def home(request: Request):
    news = crud.get_all_news()
    return templates.TemplateResponse("index.html", {"request": request, "news": news})


@app.get("/admin")
async def admin_panel(request: Request):
    return templates.TemplateResponse(
        "admin.html", {"request": request, "auto_update_enabled": auto_update_enabled}
    )


@app.post("/admin")
async def handle_admin_actions(request: Request):
    global auto_update_enabled, latest_news_time
    data = await request.json()

    if data.get("toggle_auto"):
        auto_update_enabled = not auto_update_enabled
        return {"status": "auto_update_toggled", "enabled": auto_update_enabled}

    elif data.get("title") and data.get("content"):
        news = schemas.NewsCreate(title=data["title"], content=data["content"])
        db_news = crud.create_news(news)
        latest_news_time = datetime.now(timezone.utc)

        for conn in crud.active_connections:
            await conn.send_json({"title": db_news.title, "content": db_news.content})
        return {"status": "news_added"}

    return {"status": "no_action"}


@app.websocket("/ws/news")
async def websocket_news(websocket: WebSocket):
    await websocket.accept()
    crud.active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        if websocket in crud.active_connections:
            crud.active_connections.remove(websocket)


async def auto_news_generator():
    global auto_update_enabled, latest_news_time
    while True:
        if auto_update_enabled:
            try:
                news_list, newest_time = await get_latest_news(latest_news_time)
                if news_list:
                    latest_news_time = newest_time
                    for title, content in news_list:
                        news = schemas.NewsCreate(title=title, content=content)
                        db_news = crud.create_news(news)
                        for conn in crud.active_connections:
                            await conn.send_json(
                                {"title": db_news.title, "content": db_news.content}
                            )
            except Exception as e:
                print(f"Auto-update error: {e}")
        await asyncio.sleep(10)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_news_generator())
