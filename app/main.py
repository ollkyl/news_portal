from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import asyncio
from datetime import datetime, timezone
from app.db import Base, engine
from app import crud, schemas, state
from app.parser import get_latest_news
from app.routers import admin, homepage


app = FastAPI()
app.include_router(admin.router)
app.include_router(homepage.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

Base.metadata.create_all(bind=engine)

auto_update_enabled = False
latest_news_time = datetime.now(timezone.utc)


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
    while True:
        if state.auto_update_enabled:
            try:
                news_list, newest_time = await get_latest_news(state.latest_news_time)
                if news_list:
                    state.latest_news_time = newest_time
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
