from rest_framework import serializers

from .utils import get_all_articles, get_article_by_slug

class ArticlesSerializer(serializers.Serializer):

    articles = serializers.SerializerMethodField()
    pagination = serializers.SerializerMethodField()

    def _get_data(self):

        if not hasattr(self, "_cached_data"):

            sort = self.context.get("sort")
            page = self.context.get("page", 1)

            self._cached_data = get_all_articles(sort=sort, page=page)

        return self._cached_data

    def get_articles(self, obj):

        return self._get_data().get("articles", [])

    def get_pagination(self, obj):
        
        return self._get_data().get("pagination", {})
    
class ArticleBySlugSerializer(serializers.Serializer):
    
    article = serializers.SerializerMethodField()

    def get_article(self, obj):

        slug = self.context.get("slug")

        data = get_article_by_slug(slug)

        if "error" in data:

            return data

        return data

