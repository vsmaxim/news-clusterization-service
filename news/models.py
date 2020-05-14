from typing import List, Dict

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone
from news_clustering.nlp import sentence_embedder, text_embedder


class ArticleManager(models.Manager):
    def articles_from_time_window(self, dtm: timezone.datetime, time_window: int = 180):
        delta = timezone.timedelta(days=time_window)
        return self.get_queryset().filter(publish_date__gt=dtm - delta, publish_date__lt=dtm + delta)

    def cluster_new_articles(self, articles_clusters: List[List[int]]):
        for article_ids in articles_clusters:
            cluster = Cluster.objects.create()
            self.get_queryset().filter(id__in=article_ids).update(cluster_id=cluster.id)

    def extend_old_clusters(self, articles_mapping: Dict[int, List[int]]):
        for cluster_id, article_ids in articles_mapping.items():
            self.get_queryset().filter(id__in=article_ids).update(cluster_id=cluster_id)


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
    objects = ArticleManager()

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
