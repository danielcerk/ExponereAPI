from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.catalog.views import CatalogViewSet

from .views import (
    MetaPixelViewSet,
    TagManagerViewSet,
    GA4ViewSet,
)

router = DefaultRouter()
router.register(r"", CatalogViewSet, basename="catalogs")

urlpatterns = [

    path("", include(router.urls)),

    path(
        "<int:catalog_pk>/plugin/marketing/meta-pixel/",
        MetaPixelViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
        }),
        name="catalog-meta-pixel",
    ),

    path(
        "<int:catalog_pk>/plugin/marketing/tag-manager/",
        TagManagerViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
        }),
        name="catalog-tag-manager",
    ),

    path(
        "<int:catalog_pk>/plugin/marketing/ga4/",
        GA4ViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
        }),
        name="catalog-ga4",
    ),

]