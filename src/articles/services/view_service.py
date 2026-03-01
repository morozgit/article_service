from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone


class ViewService:
    BUCKET_PREFIX = "article:views:"
    BUCKET_TTL = 60 * 60 * 25  # 25 часов

    @staticmethod
    def _get_current_bucket_key():
        now = timezone.now()
        return f"{ViewService.BUCKET_PREFIX}{now.strftime('%Y%m%d%H')}"

    @staticmethod
    def register_view(article_id: int):
        redis = cache.client.get_client(write=True)
        bucket_key = ViewService._get_current_bucket_key()
        redis.hincrby(bucket_key, article_id, 1)
        redis.expire(bucket_key, ViewService.BUCKET_TTL)

    @staticmethod
    def get_popular_articles(top_n=10):
        redis = cache.client.get_client()
        now = timezone.now()

        keys = [
            f"{ViewService.BUCKET_PREFIX}{(now - timedelta(hours=i)).strftime('%Y%m%d%H')}"
            for i in range(24)
        ]

        article_counts = {}
        for key in keys:
            data = redis.hgetall(key)
            for k, v in data.items():
                aid = int(k)
                cnt = int(v)
                article_counts[aid] = article_counts.get(aid, 0) + cnt

        top_articles = sorted(article_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return top_articles