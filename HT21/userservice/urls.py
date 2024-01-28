from django.urls import (
    path,
    include
)

from rest_framework import routers

from . import api_views
from . import views
# Create your views here.

app_name = 'products'

router = routers.DefaultRouter()

# router.register(r'api/cart', api_views.ListAPIView, basename='cart')
# router.register(r'api/admin/product', api_views.ProductViewSet)
# router.register(r'api/category', api_views.CategoryReadOnlyModelViewSet)
# router.register(r'api/admin/category', api_views.CategoryViewSet)

app_name = 'userservice'

urlpatterns = [
    # public

    # registered users
    path('cart', views.CartListView.as_view(),
         name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart,
         name='remove_from_cart'),
    path('clear_cart', views.flush_cart, name='flush_cart'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),

    # admin

    # api
    path('api/cart/', api_views.CartListView.as_view(), name='api_cart_list'),
    path('api', include(router.urls)),
]

urlpatterns += router.urls
