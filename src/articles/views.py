from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.view_service import ArticleService
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.cache import cache


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@api_view(["POST"])
def register_view_api(request, pk):
    article = get_object_or_404(Article, pk=pk)
    ArticleService.register_view(article.id)
    return Response({"status": "view registered"})


@api_view(["GET"])
def popular_articles(request):
    top_n = int(request.query_params.get("top", 10))
    top_list = ArticleService.get_popular_articles(top_n=top_n)
    article_ids = [aid for aid, _ in top_list]

    articles = Article.objects.filter(id__in=article_ids)
    serializer = ArticleSerializer(articles, many=True)

    article_dict = {a['id']: a for a in serializer.data}
    result = []
    for aid, count in top_list:
        item = article_dict.get(aid)
        if item:
            item['views_last_24h'] = count
            result.append(item)

    return Response(result)