from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from django.contrib.auth.models import User
from products.tests import factories

admin_pass = 'adminadmin'
admin_login = 'admin'


valid_data = {
    'name': 'new name'
}


class CategoryAdminTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username=admin_login,
            password=admin_pass
        )
        self.client.force_authenticate(user=self.user)

    def test_get_product_list(self):
        categories = factories.CategoryFactory.create_batch(size=3)
        response = self.client.get(
            path=reverse('products:category_adminAPI-list'))
        expected_response = [
            {"name": category.name} for category in categories
        ]

        self.assertEqual(
            first=3,
            second=len(response.json()),
            msg='Response contain unexpected mount of categories.\n'
            f'expected: {expected_response}\n\n\n'
            f'got: {response.json()}'
        )

        self.assertCountEqual(
            expected_response,
            response.json(),
            msg='Categories differs from expected :'
            f'expected: {expected_response} '
            f'got: {response.json()} '
        )

    def test_get_category_detail(self):
        category = factories.CategoryFactory()
        response = self.client.get(
            path=reverse('products:category_adminAPI-detail',
                         kwargs={'pk': category.name}))

        expected_response = {
            "name": category.name,
        }

        self.assertDictEqual(
            expected_response,
            response.json(),
            msg="Response contains unexpected category",
        )

    def test_put_category(self):
        category = factories.CategoryFactory()
        response = self.client.put(
            path=reverse('products:category_adminAPI-detail',
                         kwargs={'pk': category.name}),
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
