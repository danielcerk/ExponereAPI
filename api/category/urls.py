from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import CategoryViewSet, BusinessCategoryViewSet
from api.catalog.views import CatalogViewSet


router = DefaultRouter()
router.register(r"", CatalogViewSet, basename="catalogs")

catalog_router = NestedDefaultRouter(
    router,
    r"",
    lookup="catalog",
)

catalog_router.register(
    r"categories",
    CategoryViewSet,
    basename="catalog-categories",
)

catalog_router.register(
    r"business-categories",
    CategoryViewSet,
    basename="catalog-business-categories",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(catalog_router.urls)),
]