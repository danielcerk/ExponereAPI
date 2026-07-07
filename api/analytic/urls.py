from django.urls import path

from .views import AnalyticView

urlpatterns = [

    path(
        "analytic/",
        AnalyticView.as_view(),
        name="catalog-analytic"
    ),

]