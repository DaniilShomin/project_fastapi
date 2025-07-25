import typing
from typing import Optional
from urllib.parse import urlparse

import validators
from fastapi import Request


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append(
        {"message": message, "category": category}
    )


def get_flashed_messages(request: Request) -> list:
    return (
        request.session.pop("_messages")
        if "_messages" in request.session
        else []
    )


def normalized_urls(url: str) -> str:
    data_url = urlparse(url)
    if data_url.netloc:
        result = data_url.scheme + "://" + data_url.netloc
    else:
        result = data_url.scheme + "://" + data_url.hostname
    return result


def not_correct_url(url: str) -> Optional[str]:
    if not url:
        return "URL обязателен"
    if len(url) > 255 or not validators.url(url):
        return "Некорректный URL"
    return None
