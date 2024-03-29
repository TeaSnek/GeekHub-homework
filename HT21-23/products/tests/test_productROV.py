from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.tests import factories


class ProductROVTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test_get_product_list(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        product = factories.ProductFactory.create(
            category=product_categories)
        response = self.client.get(
            path=reverse('products:productROAPI-list'))
        expected_response = {
            "product_name": product.product_name,
            "price": f'{product.price:.2f}',
            "sears_id": product.sears_id,
            "short_about": product.short_about,
            "brand": product.brand,
            "category": [
                str(category) for category in product_categories
            ],
            "sears_link": product.sears_link
        }

        self.assertEqual(
            first=1,
            second=len(response.json()),
            msg='Response contain too many products.\n'
            f'expected: {[expected_response]}\n\n\n'
            f'got: {response.json()}'
        )

        for field in expected_response.keys():
            if field == 'category':
                continue
            self.assertEqual(
                expected_response[field],
                response.json()[0][field],
                msg=f'Response {field} differs from expected: '
                f'expected: {expected_response[field]} '
                f'got: {response.json()[0][field]} '
            )

        self.assertCountEqual(
            expected_response['category'],
            response.json()[0]['category'],
            msg='Products categories differs from expected :'
            f'expected: {expected_response["category"]} '
            f'got: {response.json()[0]["category"]} '
        )

    def test_get_product_detail(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        product = factories.ProductFactory.create(
            category=product_categories)
        response = self.client.get(
            path=reverse('products:productROAPI-detail',
                         kwargs={'pk': product.sears_id}))

        expected_response = {
            "product_name": product.product_name,
            "price": f'{product.price:.2f}',
            "sears_id": product.sears_id,
            "short_about": product.short_about,
            "brand": product.brand,
            "category": [
                str(category) for category in product_categories
            ],
            "sears_link": product.sears_link
        }

        for field in expected_response.keys():
            if field == 'category':
                continue
            self.assertEqual(
                expected_response[field],
                response.json()[field],
                msg=f'Response {field} differs from expected: '
                f'expected: {expected_response[field]} '
                f'got: {response.json()[field]} '
            )

        self.assertCountEqual(
            expected_response['category'],
            response.json()['category'],
            msg='Products categories differs from expected :'
            f'expected: {expected_response["category"]} '
            f'got: {response.json()["category"]} '
        )
