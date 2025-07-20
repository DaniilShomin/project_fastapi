from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    checks = relationship("UrlCheck", back_populates="url")


class UrlCheck(Base):
    __tablename__ = "url_checks"

    id = Column(Integer, primary_key=True)
    url_id = Column(
        Integer, ForeignKey("urls.id", ondelete="CASCADE"), nullable=False
    )
    status_code = Column(Integer)
    h1 = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    url = relationship("Url", back_populates="checks")
