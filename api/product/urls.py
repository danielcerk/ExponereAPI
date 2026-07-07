from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.catalog.views import CatalogViewSet
from .views import ProductViewSet

router = DefaultRouter()
router.register(r"", CatalogViewSet, basename="catalogs")

catalog_router = NestedDefaultRouter(
    router,
    r"",
    lookup="catalog",
)

catalog_router.register(
    r"products",
    ProductViewSet,
    basename="catalog-products",
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(catalog_router.urls)),
]