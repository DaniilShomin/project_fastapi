from sqlalchemy import text
from page_analyzer.models.database import session_factory
from page_analyzer.models.models import Url, UrlCheck


class UrlReposetory:
    def __init__(self):
        self.conn = session_factory()

    def get_content(self, reversed=False):
        with self.conn as session:
            if reversed:
                urls = session.query(Url).order_by(text("id DESC")).all()
            else:
                urls = session.query(Url).all()
            return urls

    def find(self, id):
        with self.conn as session:
            url = session.query(Url).filter_by(id=id).first()
            return url if url else None

    def save(self, url):
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)

    def _update(self, url):
        with self.conn as session:
            url_update = self.find(url["id"])
            if url["name"]:
                url_update.name = url["name"]
            if url["created_at"]:
                url_update.created_at = url["created_at"]

        session.add(url_update)
        session.commit()

    def _create(self, url) -> Url:
        with self.conn as session:
            url = Url(
                name=url["name"],
            )
            session.add(url)
            session.commit()
            return url

    def get_by_name(self, name):
        with self.conn as session:
            url = session.query(Url).filter_by(name=name).first()
            return url if url else None


class UrlCheckReposetory:
    def __init__(self):
        self.conn = session_factory()

    def get_add(self, data):
        new_check = UrlCheck(
            url_id=data["url_id"],
            status_code=data["status_code"],
            h1=data["h1"],
            title=data["title"],
            description=data["description"],
        )
        with self.conn as session:
            session.add(new_check)
            session.commit()

    def get_content(self, id, reversed=False):
        with self.conn as session:
            if reversed:
                check_urls = (
                    session.query(UrlCheck)
                    .filter_by(id=id)
                    .order_by(text("id DESC"))
                    .all()
                )
            else:
                check_urls = session.query(UrlCheck).filter_by(id=id).all()
            return check_urls
