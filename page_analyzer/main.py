from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from page_analyzer.api.urls import UrlsRouter
from page_analyzer.modules import get_flashed_messages
from page_analyzer.config import settings


app = FastAPI(
    middleware=[
        Middleware(
            SessionMiddleware,
            secret_key=settings.SECRET_KEY,
            session_cookie="session",
        )
    ],
    debug=settings.DEBUG,
)

templates = Jinja2Templates(
    directory=settings.TEMPLATES_DIR,
    auto_reload=settings.AUTO_RELOAD_TEMPLATES,
)
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@app.get("/")
async def index(request: Request):
    message = get_flashed_messages(request)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": message,
        },
    )


urls_views = UrlsRouter(templates)
app.include_router(urls_views.router)
