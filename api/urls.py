from django.urls import path, include

urlpatterns = [

    path('auth/', include('api.auth.urls')),
    path('catalogs/', include('catalog.urls')),
    path('catalogs/', include('category.urls')),
    path('catalogs/', include('product.urls')),
    path('panel/subscription/', include('api.subscription.urls')),

]