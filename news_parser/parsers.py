from dataclasses import dataclass
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
import feedparser
import newspaper
import requests

from news_parser.db.models import Article
from news_parser.api.vk import get_latest_posts_links


@dataclass
class RSSFeedEntry:
    title: str
    summary: str
    link: str
    pub_date: datetime


def parse_rss_entries(rss: str) -> List[RSSFeedEntry]:
    feed = feedparser.parse(rss)
    entries = feed['entries']
    return [RSSFeedEntry(entry['title'], entry['summary'], entry['link'], entry['published_parsed']) for entry in entries]


def parse_articles_from_rss(rss: str) -> List[Article]:
    articles: List[Article] = []
    entries = parse_rss_entries(rss)

    for entry in entries:
        # TODO: Probably extend to another languages
        article = newspaper.Article(entry.link, language='ru')
        article.download()
        article.parse()
        articles.append(Article(
            title=entry.title,
            text=article.text,
            source=entry.link,
            publish_date=entry.pub_date,
        ))
    
    return articles


def parse_articles_from_vk_source(public_id: int, days_count: int) -> Article:
    links = get_latest_posts_links(public_id, days_count)
    articles: List[Article] = []

    for link in links:
        article = newspaper.Article(link, language='ru')
        article.download()
        article.parse()
        articles.append(Article(
            title=article.title,
            text=article.text,
            source=link,
            publish_date=article.publish_date,
        ))

    return articles