from datetime import datetime
from unittest.mock import patch
import fakeredis
import pytest
from django.urls import reverse
from articles.models import Article

from articles.services.view_service import ArticleService

@pytest.mark.django_db
def test_get_articles(api_client):
    url = reverse('article-list')
    response = api_client.get(url, format='json')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_articles(api_client):
    url = reverse('article-list')

    payload = {
        'title': 'Test article',
        'content': 'Test content',
    }

    api_client.post(url, payload, format='json')
    response_create = api_client.get(url, format='json')
    assert response_create.status_code == 200
    assert len(response_create.data) == 1
    assert response_create.data[0]['title'] == 'Test article'
    assert response_create.data[0]['content'] == 'Test content'
    created_at_str = response_create.data[0]['created_at']
    created_at_dt = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
    assert isinstance(created_at_dt, datetime)

    response = api_client.get(url, format='json')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1


@pytest.mark.django_db
def test_article_views_count_mocked(api_client):
    article = Article.objects.create(title="Test article", content="Test content")
    url = reverse('article-view', kwargs={'pk': article.id})

    with patch.object(ArticleService, 'register_view') as mock_view:
        for _ in range(3):
            api_client.post(url, format='json')

        assert mock_view.call_count == 3


@pytest.mark.django_db
def test_popular_articles(api_client, monkeypatch):
    article1 = Article.objects.create(title="Article 1", content="Content 1")
    article2 = Article.objects.create(title="Article 2", content="Content 2")
    article3 = Article.objects.create(title="Article 3", content="Content 3")

    fake_redis = fakeredis.FakeStrictRedis()
    monkeypatch.setattr("django.core.cache.cache.client.get_client", lambda write=False: fake_redis)

    for _ in range(3):
        ArticleService.register_view(article1.id)
    for _ in range(2):
        ArticleService.register_view(article2.id)
    ArticleService.register_view(article3.id)

    url = reverse('popular-articles')
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['id'] == article1.id
    assert response.data[1]['id'] == article2.id
    assert response.data[2]['id'] == article3.id

    views_in_response = [item['views_last_24h'] for item in response.data]
    assert views_in_response == [3, 2, 1]