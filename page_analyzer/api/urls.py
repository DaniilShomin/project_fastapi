from datetime import date
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from page_analyzer.modules import (
    flash,
    get_flashed_messages,
    normalized_urls,
    not_correct_url,
)
from page_analyzer.repositories.url_reposetory import (
    UrlCheckReposetory,
    UrlReposetory,
)


class UrlsRouter:
    def __init__(self, templates):
        self.templates = templates
        self.router = APIRouter(prefix="/urls", tags=["urls"])
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route("/", self.urls_get, methods=["GET"])
        self.router.add_api_route("/", self.urls_post, methods=["POST"])

    async def urls_get(self, request: Request):
        repo = UrlReposetory()
        urls = repo.get_content(reversed=True)
        check_repo = UrlCheckReposetory()
        for url in urls:
            check_url = check_repo.get_content(url.id, reversed=True)
            if check_url:
                url["last_check"] = check_url[0]["created_at"]
                url["status_code"] = check_url[0]["status_code"]
            else:
                url.last_check = ""
                url.status_code = ""
        messages = get_flashed_messages(request)
        return self.templates.TemplateResponse(
            "urls/index.html",
            {"request": request, "messages": messages, "urls": urls},
        )

    async def urls_post(self, request: Request):
        form_data = await request.form()
        url = form_data.get("url")
        error = not_correct_url(url)
        if error:
            flash(request, f"{error}", "danger")
            messages = get_flashed_messages(request)
            return self.templates.TemplateResponse(
                "index.html",
                {"request": request, "messages": messages, "url": url},
            )
        repo = UrlReposetory()
        norm_url = {"name": normalized_urls(url), "created_at": date.today()}
        url_in_repo = repo.get_by_name(norm_url["name"])
        if url_in_repo:
            flash(request, "Страница уже существует", "info")
            return RedirectResponse(url="/", status_code=303)
        else:
            repo.save(norm_url)
            flash(request, "Страница успешно добавлена", "success")
        return RedirectResponse(url="/", status_code=303)
