from sqlalchemy import create_engine

from news_parser.parser.config import config


db_config = config['db']
engine = create_engine(f'postgresql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}/{db_config["database"]}')
