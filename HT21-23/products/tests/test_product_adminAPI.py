from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from django.contrib.auth.models import User
from products.tests import factories


admin_login = 'admin'
admin_pass = 'adminadmin'


valid_data = {
                "product_name": "prod",
                "price": "101.92",
                "sears_id": "asdasdlaisdfd",
                "short_about": "CHARGER STARTER",
                "brand": "Milwaukee",
                "sears_link": "https://www.sears.com/milw-star/p-A013824497",
            }


class ProductAdminTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username=admin_login,
            password=admin_pass
        )
        self.client.force_authenticate(user=self.user)

    def test_get_product_list(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        product = factories.ProductFactory.create(
            category=product_categories)
        response = self.client.get(
            path=reverse('products:product_adminAPI-list'))
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
            path=reverse('products:product_adminAPI-detail',
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

    def test_put_product(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        product = factories.ProductFactory.create(
            category=product_categories)
        response = self.client.put(
            path=reverse('products:product_adminAPI-detail',
                         kwargs={'pk': product.sears_id}),
            data=valid_data,
        )

        self.assertEqual(response.status_code, 200,
                         msg=f'Returned response status code {response.status_code}')

        for field in valid_data.keys():
            self.assertEqual(
                valid_data[field],
                response.json()[field],
                msg=f'Response {field} doesnt match: '
                f'expected {valid_data[field]} | got {response.json()[field]}'
            )
