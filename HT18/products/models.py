from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sears_id = models.CharField(primary_key=True, max_length=200)
    short_about = models.TextField(default='')
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    sears_link = models.URLField()

    def __str__(self) -> str:
        return self.product_name
