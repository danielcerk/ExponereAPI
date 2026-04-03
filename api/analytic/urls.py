from django.urls import path

from .views import AnalyticView

urlpatterns = [

    path(
        "<int:catalog_id>/analytic/",
        AnalyticView.as_view(),
        name="catalog-analytic"
    ),

]