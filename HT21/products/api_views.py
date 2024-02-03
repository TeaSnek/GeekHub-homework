from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from . import models
from . import serializers


class ProductReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        model_fields_name = [field.name for field
                             in models.Product._meta.get_fields()]
        params = {key: value for key, value in self.request.data.items()
                  if key in model_fields_name}
        if not params:
            return models.Product.objects.all()
        return models.Product.objects.filter(**params)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        model_fields_name = [field.name for field
                             in models.Product._meta.get_fields()]
        params = {key: value for key, value in self.request.data.items()
                  if key in model_fields_name}
        if not params:
            return models.Product.objects.all()
        return models.Product.objects.filter(**params)


class CategoryReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Categorys to be viewed or edited.
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        model_fields_name = [field.name for field
                             in models.Category._meta.get_fields()]
        params = {key: value for key, value in self.request.data.items()
                  if key in model_fields_name}
        if not params:
            return models.Category.objects.all()
        return models.Category.objects.filter(**params)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categorys to be viewed or edited.
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        model_fields_name = [field.name for field
                             in models.Category._meta.get_fields()]
        params = {key: value for key, value in self.request.data.items()
                  if key in model_fields_name}
        if not params:
            return models.Category.objects.all()
        return models.Category.objects.filter(**params)
