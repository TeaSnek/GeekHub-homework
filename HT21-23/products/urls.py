from django.urls import (
    path,
    include,
)
from rest_framework import routers

from . import views
from . import api_views
# Create your views here.

app_name = 'products'

router = routers.DefaultRouter()

router.register(r'api/product', api_views.ProductReadOnlyModelViewSet,
                basename='productROAPI')
router.register(r'api/admin/product', api_views.ProductViewSet,
                basename='product_adminAPI')
router.register(r'api/category', api_views.CategoryReadOnlyModelViewSet,
                basename='categoryROAPI')
router.register(r'api/admin/category', api_views.CategoryViewSet,
                basename='category_adminAPI')

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

    # api
    path('', include(router.urls)),
]

urlpatterns += router.urls
