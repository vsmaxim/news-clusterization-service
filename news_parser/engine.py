from sqlalchemy import create_engine

engine = create_engine('postgresql://news_parser:news_parser@localhost/news_parser')
