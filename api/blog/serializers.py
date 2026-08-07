from rest_framework import serializers

from .utils import get_all_articles, get_article_by_slug

from .models import Post

class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "slug",
            "image",
            "content",
            "author",
            "is_published",
            "published_at",
            "created_at",
            "updated_at",
        ]


class ArticleBySlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "slug",
            "image",
            "content",
            "author",
            "is_published",
            "published_at",
            "created_at",
            "updated_at",
        ]

