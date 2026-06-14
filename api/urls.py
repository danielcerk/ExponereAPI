from django.urls import path, include

urlpatterns = [

    path('auth/', include('api.auth.urls')),
    path('blog/', include('api.blog.urls')),
    path('catalogs/', include('api.AI.urls')),
    path('catalogs/', include('api.catalog.urls')),
    path('', include('api.category.urls')),
    path('catalogs/', include('api.coupon.urls')),
    path('catalogs/', include('api.customer.urls')),
    path('catalogs/', include('api.marketing.urls')),
    path('', include('api.analytic.urls')),
    path('catalogs/', include('api.notification.urls')),
    path('catalogs/', include('api.order.urls')),
    path('catalogs/', include('api.product.urls')),
    path('catalogs/', include('api.wishlist.urls')),
    path('status/', include('api.status.urls')),
    path('panel/subscription/', include('api.subscription.urls')),
    path('newsletter/', include('api.newsletter.urls')),

]