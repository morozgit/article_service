from django.urls import path

from .views import ArticleListCreateView, popular_articles, register_view_api

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list"),
    path("articles/<int:pk>/view/", register_view_api, name="article-view"),
    path("articles/popular/", popular_articles, name="popular-articles"),
]
