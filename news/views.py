from rest_framework.generics import RetrieveAPIView

from news.models import Article, Cluster
from news.serializers import ArticleSerializer, ClusterSerializer
from news_clustering.parsers import parse_article_from_link


class ArticleRetrieveView(RetrieveAPIView):
    serializer_class = ArticleSerializer

    def get_object(self):
        source = self.request.query_params["source"]
        articles = Article.objects.filter(source=source).first()
        return articles.first() or parse_article_from_link(source)


class AssociatedArticlesRetrieveView(RetrieveAPIView):
    serializer_class = ClusterSerializer

    # TODO: Handle null pk
    def get_queryset(self):
        article = Article.objects.get(pk=self.kwargs["pk"])
        return Article.objects.filter(cluster_id=article)


class ClusterRetrieveView(RetrieveAPIView):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()
