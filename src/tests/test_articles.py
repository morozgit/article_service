from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_articles(api_client):
    url = reverse('article-list')
    response = api_client.get(url, format='json')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0
