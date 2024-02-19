from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.tests import factories


class CategoryROVTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test_get_category_list(self):
        categories = factories.CategoryFactory.create_batch(size=3)
        response = self.client.get(
            path=reverse('products:categoryROAPI-list'))
        expected_response = [
            {"name": category.name} for category in categories]

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
            path=reverse('products:categoryROAPI-detail',
                         kwargs={'pk': category.name}))

        expected_response = {
            "name": category.name,
        }

        self.assertDictEqual(
            expected_response,
            response.json(),
            msg="Response contains unexpected category",
        )
