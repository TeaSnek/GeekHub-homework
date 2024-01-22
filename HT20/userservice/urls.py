from django.urls import path
from . import views

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
]
