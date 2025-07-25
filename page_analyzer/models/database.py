from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from page_analyzer.config import settings
from page_analyzer.models.models import Base

engine = create_engine(settings.DB_URL)

session_factory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
