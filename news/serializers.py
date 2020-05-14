from rest_framework import serializers
from news.models import Article, Cluster


class ArticleSerializer(serializers.Serializer):

    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'source',
            'publish_date',
            'cluster',
            'cluster_difference',
        )


class ClusterSerializer(serializers.Serializer):

    class Meta:
        model = Cluster
        fields = (
            'title',
            'id',
        )
