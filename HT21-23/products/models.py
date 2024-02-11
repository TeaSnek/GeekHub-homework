from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sears_id = models.CharField(primary_key=True, max_length=200)
    short_about = models.TextField(default='')
    brand = models.CharField(max_length=200)
    category = models.ManyToManyField(
        'Category',
        blank=True,
        related_name='products',
    )
    sears_link = models.URLField()

    def __str__(self) -> str:
        return self.product_name
