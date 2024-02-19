from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from django.contrib.auth.models import User
from products.tests import factories

user_pass = 'useruser'
user_login = 'user'


class CartApiTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username=user_pass,
            password=user_login
        )
        self.url = reverse('userservice:api_cart_list')
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_add_to_cart(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        products = [factories.ProductFactory.create(
            category=[category,]) for category in product_categories]
        response = self.client.post(
            self.url,
            data={
                'action': 'add',
                products[0].sears_id: 1
            }
        )

        self.assertEqual(
            200,
            response.status_code,
        )

    def test_remove_from_cart(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        products = [factories.ProductFactory.create(
            category=[category,]) for category in product_categories]
        response = self.client.post(
            self.url,
            data={
                'action': 'remove',
                products[0].sears_id: True,
            }
        )

        self.assertEqual(
            200,
            response.status_code,
        )

    def test_change_quantity(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        products = [factories.ProductFactory.create(
            category=[category,]) for category in product_categories]
        response = self.client.post(
            self.url,
            data={
                'action': 'update',
                products[0].sears_id: 3,
            }
        )

        self.assertEqual(
            200,
            response.status_code,
        )

    def test_get_cart(self):
        product_categories = factories.CategoryFactory.create_batch(size=3)
        products = [factories.ProductFactory.create(
            category=[category,]) for category in product_categories]
        self.client.post(
            self.url,
            data={
                'action': 'add',
                products[0].sears_id: 1,
                products[1].sears_id: 3,
                products[2].sears_id: 10,
            }
        )
        response = self.client.get(self.url)

        self.assertEqual(
            3,
            response.json()[1]["quantity"]
        )
        self.client.post(
            self.url,
            data={
                'action': 'update',
                products[2].sears_id: -2,
            }
        )
        response = self.client.get(self.url)

        self.assertEqual(
            8,
            response.json()[2]["quantity"]
        )
