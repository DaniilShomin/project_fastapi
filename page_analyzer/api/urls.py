from datetime import date

import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from page_analyzer.modules import (
    flash,
    get_flashed_messages,
    normalized_urls,
    not_correct_url,
)
from page_analyzer.repositories.url_repository import (
    UrlCheckRepository,
    UrlRepository,
)


class UrlsRouter:
    def __init__(self, templates):
        self.templates = templates
        self.router = APIRouter(prefix="/urls", tags=["urls"])
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route("/", self.urls_list, methods=["GET"])
        self.router.add_api_route("/", self.urls_post, methods=["POST"])
        self.router.add_api_route("/{id}/", self.urls_show, methods=["GET"])
        self.router.add_api_route(
            "/{id}/check", self.urls_check, methods=["POST"]
        )

    async def urls_list(self, request: Request):
        repo = UrlRepository()
        urls = repo.get_content(reversed=True)
        check_repo = UrlCheckRepository()
        for url in urls:
            check_url = check_repo.get_content(url.id, reversed=True)
            if check_url:
                url.last_check = check_url[0].created_at
                url.status_code = check_url[0].status_code
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
        repo = UrlRepository()
        norm_url = {"name": normalized_urls(url), "created_at": date.today()}
        url_in_repo = repo.get_by_name(norm_url["name"])
        if url_in_repo:
            flash(request, "Страница уже существует", "info")
            return RedirectResponse(
                url=request.url_for("index"), status_code=303
            )
        else:
            saved_url = repo.save(norm_url)
            flash(request, "Страница успешно добавлена", "success")
            print(saved_url)
        return RedirectResponse(
            url=request.url_for("urls_show", id=saved_url.id), status_code=303
        )

    async def urls_show(self, id: int, request: Request):
        repo = UrlRepository()
        check_repo = UrlCheckRepository()
        url = repo.find(id)
        checks_url = check_repo.get_content(id=id, reversed=True)
        print(checks_url)
        messages = get_flashed_messages(request)
        return self.templates.TemplateResponse(
            "urls/show.html",
            {
                "request": request,
                "messages": messages,
                "url": url,
                "checks_url": checks_url,
            },
        )

    async def urls_check(self, id: int, request: Request):
        repo = UrlRepository()
        url = repo.find(id)
        error = False
        try:
            async with httpx.AsyncClient() as client:
                auth = httpx.BasicAuth("user", "pass")
                req = await client.get(
                    url.name,
                    timeout=httpx.Timeout(2.0),
                    auth=auth,
                    follow_redirects=True,
                )
        except Exception:
            error = True
            flash(request, "Произошла ошибка при проверке", "danger")
        if not error:
            soup = BeautifulSoup(req.text, "html.parser")
            extracted_h1 = soup.h1.string if soup.h1 else ""
            extracted_title = soup.title.string if soup.title else ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            extracted_description = meta_tag["content"] if meta_tag else ""
            check_repo = UrlCheckRepository()
            data = {
                "url_id": id,
                "status_code": req.status_code,
                "h1": extracted_h1,
                "title": extracted_title,
                "description": extracted_description,
                "created_at": date.today(),
            }
            check_repo.get_add(data)
            flash(request, "Страница успешно проверена", "success")
        return RedirectResponse(
            url=request.url_for("urls_show", id=id), status_code=303
        )
