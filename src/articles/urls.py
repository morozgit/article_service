from django.urls import path
from .views import ArticleListCreateView, register_view_api, popular_articles

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list"),
    path("articles/<int:pk>/view/", register_view_api, name="article-view"),
    path("articles/popular/", popular_articles, name="popular-articles"),
]