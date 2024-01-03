from django.urls import path

from . import views
# Create your views here.

app_name = 'products'

urlpatterns = [
    path('', views.LandingTemplateView.as_view(), name='landing'),
    path('products', views.ProductsListView.as_view(), name='products_list'),
    path('detail/<str:pk>', views.ProductDetailView.as_view(),
         name='product_detail'),
    path('add_products', views.AddProductsFormView.as_view(),
         name='add_products')
]
