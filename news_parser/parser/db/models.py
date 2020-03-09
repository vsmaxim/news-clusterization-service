from news_parser.parser.db.mapping import Base
from sqlalchemy import Column, String, Integer, DateTime


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    source = Column(String, unique=True)
    publish_date = Column(DateTime)


class NewsSource(Base):
    __tablename__ = 'news_sources'

    id = Column(Integer, primary_key=True)
    rss_url = Column(String)
    vk_public_id = Column(Integer)
