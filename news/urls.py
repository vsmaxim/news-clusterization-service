from django.urls import path
from news import views

urlpatterns = [
    path("articles/analytics/", views.ArticleRetrieveView.as_view()),
    path("articles/<int:pk>/similar/", views.AssociatedArticlesRetrieveView.as_view()),
    path("cluster/<int:pk>/", views.ClusterRetrieveView.as_view()),
]
