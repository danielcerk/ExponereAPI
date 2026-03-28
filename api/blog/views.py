from django.shortcuts import render

from .serializers import ArticleBySlugSerializer, ArticlesSerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ArticlesView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        sort = request.query_params.get("sort")
        page = request.query_params.get("page", 1)

        serializer = ArticlesSerializer(

            context={

                "sort": sort,
                "page": int(page)

            }

        )

        return Response(serializer.data)

class ArticleView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        slug = self.kwargs.get("post_slug")

        serializer = ArticleBySlugSerializer(

            context={"slug": slug}

        )

        return Response(serializer.data)

