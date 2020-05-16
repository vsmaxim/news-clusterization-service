from rest_framework import serializers
from news.models import Article, Cluster


class SentenceProbabilitySerializer(serializers.Serializer):
    sentence = serializers.CharField()
    difference = serializers.FloatField()


class ArticleSerializer(serializers.Serializer):
    cluster_difference_probs = SentenceProbabilitySerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'source',
            'publish_date',
            'cluster',
            'cluster_difference_probs',
        )


class ClusterSerializer(serializers.Serializer):

    class Meta:
        model = Cluster
        fields = (
            'title',
            'id',
        )
