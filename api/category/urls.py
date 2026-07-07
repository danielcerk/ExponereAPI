from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (
    CategoryViewSet,
    BusinessCategoryViewSet,
    SubCategoryViewSet
)
from api.catalog.views import CatalogViewSet

router = DefaultRouter()

router.register(
    r"business-categories",
    BusinessCategoryViewSet,
    basename="business-categories",
)

router.register(
    r"catalogs",
    CatalogViewSet,
    basename="catalogs"
)

catalog_router = NestedDefaultRouter(
    router,
    r"catalogs",
    lookup="catalog",
)

catalog_router.register(
    r"categories",
    CategoryViewSet,
    basename="catalog-categories",
)

category_router = NestedDefaultRouter(
    catalog_router,
    r"categories",
    lookup="category",
)

category_router.register(
    r"subcategories",
    SubCategoryViewSet,
    basename="category-subcategories",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(catalog_router.urls)),
    path("", include(category_router.urls)),
]