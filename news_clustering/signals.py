from datetime import timedelta, datetime
from typing import List, Any, Dict

import numpy as np

from news.models import Article, Cluster
from django.db.models.signals import post_save
from django.dispatch import receiver
from sklearn.cluster import AgglomerativeClustering


def _get_articles_from_time_window(
    target_date: datetime, time_window: int = 180
) -> List[Article]:
    window_delta = timedelta(days=time_window)

    return Article.objects.filter(
        created_at__gt=target_date - window_delta,
        created_at__lt=target_date + window_delta,
    )


def _create_clusters_from_article_ids(article_ids: List[int]):
    raise NotImplementedError


def _extend_old_clusters_with_new_articles(cluster_articles_mapping: Dict[str, List[int]]):
    raise NotImplementedError


@receiver(post_save, sender=Article)
def clusterize_and_calc_distances(sender: Article):
    def extend_array_key(d: dict, key: str, value: Any):
        d[key] = d.get(key, []) + value

    articles_values = _get_articles_from_time_window(sender.publish_date).values_list(
        "id", "title_embedding", "cluster_id"
    )
    ids, embeddings, cluster_ids = zip(*articles_values)

    embeddings = np.array(embeddings)
    clustering = AgglomerativeClustering(linkage="single", distance_threshold=10,).fit(
        embeddings
    )
    new_clusters = clustering.labels_

    new_clusters_ids = {}
    old_cluster_members_ids = {}

    for id_, current_cluster, new_cluster in zip(ids, cluster_ids, new_clusters):
        if new_cluster != -1:
            if current_cluster is None:
                extend_array_key(new_clusters_ids, new_cluster, id_)
            else:
                extend_array_key(old_cluster_members_ids, current_cluster, id_)

    _extend_old_clusters_with_new_articles(old_cluster_members_ids)
    _create_clusters_from_article_ids(list(new_clusters_ids.values()))

    return clustering
