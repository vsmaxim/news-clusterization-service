from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

from news_clustering.parsers import parse_article_from_link
from news_clustering.nlp import sentence_embedder, text_embedder


class ArticleManager(models.Manager):
    def _parse_article(self, source: str):
        article = parse_article_from_link(source)
        article.save()
        return article

    def get_article(self, source: str):
        return self.get_queryset().filter(source=source) or self._parse_article(source)


class Article(models.Model):
    title = models.TextField()
    text = models.TextField()
    source = models.URLField(unique=True)
    publish_date = models.DateTimeField()
    cluster = models.ForeignKey(to='Cluster', null=True, on_delete=models.SET_NULL)
    cluster_difference = JSONField()
    title_embedding = ArrayField(models.FloatField())
    text_sentences = ArrayField(models.TextField())
    text_sentence_embeddings = ArrayField(ArrayField(models.IntegerField()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_embedding = sentence_embedder(self.title)
        self.text_sentence_embeddings, self.text_sentences = text_embedder(self.text)


class Cluster(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField()


class NewsSource(models.Model):
    rss_url = models.URLField()
    vk_public_id = models.IntegerField()
