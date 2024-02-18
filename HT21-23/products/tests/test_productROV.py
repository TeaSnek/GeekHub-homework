from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.tests import factories


class ProductROVTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test_get_product(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        print(product_categories)
        product = factories.ProductFactory.create(
            category=product_categories)
        response = self.client.get(path='products:products')
        expected_response = [
            {
                "product_name": product.product_name,
                "price": product.price,
                "sears_id": product.sears_id,
                "short_about": product.short_about,
                "brand": product.brand,
                "category": [
                    str(category) for category in product_categories
                ],
                "sears_link": product.sears_link
            },
        ]

        self.assertEqual(
            first=expected_response,
            second=response,
            msg=f'expected:{expected_response}\n\n\n'
            f'got:{response.request}'
        )

    def test_change_product(self):
        ...
