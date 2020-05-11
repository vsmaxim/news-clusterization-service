from rest_framework.generics import RetrieveAPIView

from news.models import Article, Cluster
from news.serializers import ArticleSerializer, ClusterSerializer


class ArticleRetrieveView(RetrieveAPIView):
    serializer_class = ArticleSerializer

    def get_object(self):
        return Article.objects.get_article(source=self.request.query_params["source"])


class AssociatedArticlesRetrieveView(RetrieveAPIView):
    serializer_class = ClusterSerializer

    # TODO: Handle null pk
    def get_queryset(self):
        article = Article.objects.get(pk=self.kwargs["pk"])
        return Article.objects.filter(cluster_id=article)


class ClusterRetrieveView(RetrieveAPIView):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()
