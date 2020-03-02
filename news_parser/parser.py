import feedparser
from bs4 import BeautifulSoup
import requests
from newspaper import Article
from typing import List
from dataclasses import dataclass


@dataclass
class RSSFeedEntry:
    title: str
    summary: str
    link: str


def parse_rss_entries(rss: str) -> List[RSSFeedEntry]:
    feed = feedparser.parse(rss)
    entries = feed['entries']
    return [RSSFeedEntry(entry['title'], entry['summary'], entry['link']) for entry in entries]


def parse_rss_article(entry: RSSFeedEntry) -> List[Article]:
    pass
