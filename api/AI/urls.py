from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.catalog.views import CatalogViewSet
from api.product.views import ProductViewSet
from .views import CopyProductViewSet, GenerateCopyView

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

product_router = NestedDefaultRouter(
    catalog_router,
    r"products",
    lookup="product",
)

product_router.register(
    r"copies",
    CopyProductViewSet,
    basename="product-copies",
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(catalog_router.urls)),
    path("", include(product_router.urls)),

    path(
        "<int:catalog_pk>/products/<int:product_pk>/generate-copy/",
        GenerateCopyView.as_view(),
        name="generate-copy",
    ),
]