from django.urls import path, include

urlpatterns = [

    path('auth/', include('api.auth.urls')),
    path('catalogs/', include('api.catalog.urls')),
    path('catalogs/', include('api.category.urls')),
    path('catalogs/', include('api.product.urls')),
    path('catalogs/', include('api.wishlist.urls')),
    path('catalogs/', include('api.qrcode.urls')),
    path('catalogs/', include('api.SEO.urls')),
    path('panel/subscription/', include('api.subscription.urls')),

]