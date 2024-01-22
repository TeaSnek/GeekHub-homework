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

    # admin
    path('update', views.update, name='update'),
    path('edit/<str:pk>', views.EditProductFormView.as_view(),
         name='edit'),
    path('delete', views.delete_view, name='delete'),
    path('add_products', views.AddProductsFormView.as_view(),
         name='add_products'),
]
