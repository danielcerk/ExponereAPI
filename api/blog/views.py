from .serializers import ArticleBySlugSerializer, ArticlesSerializer
from .models import Post

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ArticlesView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        posts = Post.objects.filter(
            is_published=True
        )

        page = request.query_params.get("page", 1)

        serializer = ArticlesSerializer(
            posts,
            many=True
        )

        return Response({
            "articles": serializer.data,
            "pagination": {
                "page": int(page),
                "count": posts.count()
            }
        })


class ArticleView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        slug = self.kwargs.get("post_slug")

        post = Post.objects.filter(
            slug=slug,
            is_published=True
        ).first()

        if not post:
            return Response(
                {
                    "error": "Post não encontrado."
                },
                status=404
            )

        serializer = ArticleBySlugSerializer(post)

        return Response({
            "article": serializer.data
        })