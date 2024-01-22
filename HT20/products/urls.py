from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.urls import path
from . import views
# Create your views here.

app_name = 'products'

urlpatterns = [
    # public
    path('', views.LandingTemplateView.as_view(), name='landing'),
    path('products', views.ProductsListView.as_view(), name='products_list'),
    path('products/<str:category>', views.ProductsListView.as_view(),
         name='category_list'),
    path('detail/<str:pk>', views.ProductDetailView.as_view(),
         name='product_detail'),

    # registered users
    path('cart', login_required(views.CartListView.as_view()),
         name='cart'),
    path('add_to_cart', login_required(views.add_to_cart), name='add_to_cart'),
    path('remove_from_cart', login_required(views.remove_from_cart),
         name='remove_from_cart'),
    path('clear_cart', login_required(views.flush_cart), name='flush_cart'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', login_required(views.logout_view), name='logout'),

    # admin
    path('update', user_passes_test(lambda u: u.is_superuser)(views.update),
         name='update'),
    path('edit/<str:pk>', user_passes_test(lambda u: u.is_superuser)(
        views.EditProductFormView.as_view()),
         name='edit'),
    path('delete', user_passes_test(lambda u: u.is_superuser)(
        views.delete_view),
         name='delete'),
    path('add_products', user_passes_test(lambda u: u.is_superuser)(
        views.AddProductsFormView.as_view()),
         name='add_products'),
]
