from django.urls import path

from .views import ArticlesView, ArticleView

urlpatterns = [

    path("articles/", ArticlesView.as_view()),
    path("articles/<slug:post_slug>/", ArticleView.as_view()),

]
