from news_parser.mapping import Base
from sqlalchemy import Column, String, Integer, DateTime


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    source = Column(String)
    publish_date = Column(DateTime)
