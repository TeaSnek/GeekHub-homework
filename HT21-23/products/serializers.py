from . import models
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['product_name', 'price', 'sears_id', 'short_about',
                  'brand', 'category', 'sears_link']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name',]
