from django.contrib.postgres.fields import JSONField
from django.db import models


class Article(models.Model):
    title = models.TextField()
    text = models.TextField()
    source = models.URLField(unique=True)
    publish_date = models.DateTimeField()
    cluster = models.ForeignKey(to='Cluster', null=True, on_delete=models.SET_NULL)
    cluster_difference = JSONField()


class Cluster(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField()


class NewsSource(models.Model):
    rss_url = models.URLField()
    vk_public_id = models.IntegerField()
