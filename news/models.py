from typing import List, Dict

import numpy as np
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone
from news_clustering.nlp import sentence_embedder, text_embedder


class ArticleManager(models.Manager):
    def articles_from_time_window(self, dtm: timezone.datetime, time_window: int = 180):
        delta = timezone.timedelta(days=time_window)
        return self.get_queryset().filter(
            publish_date__gt=dtm - delta, publish_date__lt=dtm + delta
        )

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
    publish_date = models.DateField()
    cluster = models.ForeignKey(to="Cluster", null=True, on_delete=models.SET_NULL)
    cluster_difference = ArrayField(models.FloatField(), default=list())
    title_embedding = ArrayField(models.FloatField(), default=list())
    text_sentences = ArrayField(models.TextField())
    text_sentence_embeddings = ArrayField(
        ArrayField(models.FloatField()), default=list()
    )
    objects = ArticleManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.title_embedding:
            self.title_embedding = sentence_embedder(self.title)
        if not self.text_sentence_embeddings:
            self.text_sentence_embeddings, self.text_sentences = text_embedder(
                self.text
            )

    def set_cluster_difference(self):
        cluster_articles_embeddings = (
            Article.objects.filter(cluster_id=self.cluster_id)
            .exclude(id=self.id)
            .values_list("text_sentence_embeddings", flat=True)
        )
        article_embeddings = list(map(np.array, self.text_sentence_embeddings))
        flat_cluster_embeddings = [
            np.array(emb) for embs in cluster_articles_embeddings for emb in embs
        ]

        min_distances = []

        for article_embedding in article_embeddings:
            min_distance = 10000

            for cluster_embedding in flat_cluster_embeddings:
                distance = np.linalg.norm(cluster_embedding - article_embedding)

                if distance < min_distance:
                    min_distance = distance

            min_distances.append(min_distance if flat_cluster_embeddings else 0)

        min_distances = np.array(min_distances)
        self.cluster_difference = min_distances.tolist()
        self.save()

    @property
    def cluster_difference_probs(self):
        return [
            {"sentence": sent, "difference": diff}
            for sent, diff in zip(self.text_sentences, self.cluster_difference)
        ]


class Cluster(models.Model):
    title = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class NewsSource(models.Model):
    rss_url = models.URLField()
    vk_public_id = models.IntegerField()
