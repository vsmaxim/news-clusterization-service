
from news_parser.parser.parsers import parse_articles_from_vk_source
from news_parser.parser.db.models import Article, NewsSource
from news_parser.parser.db.session import session_scope


def collect_articles_from_vk(last_days: int = 5):
    with session_scope() as session:
        for source in session.query(NewsSource):
            articles = parse_articles_from_vk_source(source.vk_public_id, last_days)
            session.add_all(articles)
            session.commit()


if __name__ == '__main__':
    collect_articles_from_vk()
