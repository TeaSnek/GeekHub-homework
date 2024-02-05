from django.http import QueryDict
from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products import models


class CartListView(APIView):
    """
    API endpoint that allows Cart to be viewed or edited.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart = request.session.get('cart', {})
        content = []
        for product_id, quantity in cart.items():
            product = models.Product.objects.get(pk=product_id)
            fields = {
                field.name: getattr(product, field.name)
                for field in product._meta.get_fields()
                if field.name != 'category'
            }
            fields['category'] = [
                str(category) for category in product.category.all()
            ]
            content.append({
                'quantity': quantity,
                'product': fields
            })
        return Response(data=content, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        cart = request.session.get('cart', {})
        if not cart:
            request.session['cart'] = {}
        data = request.data
        if isinstance(data, QueryDict):
            data = data.dict()
        try:
            action = data.pop('action')
        except KeyError:
            return Response({'message': '"action" argument is missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        match action:
            case 'add':
                for key, value in data.items():
                    if not validate_product(key):
                        return Response(
                            {'message': f'unknown product: {key}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if cart.get(key, 0):
                        request.session['cart'][key] += int(value)
                    else:
                        request.session['cart'][key] = int(value)
            case 'flush':
                if cart:
                    request.session['cart'].clear()
            case 'remove':
                for key, value in data.items():
                    if cart.get(key, ''):
                        del request.session['cart'][key]
            case 'update':
                for key, value in data.items():
                    if not validate_product(key):
                        return Response(
                            {'message': f'unknown product: {key}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if int(value) > 0:
                        if cart.get(key, 0):
                            request.session['cart'][key] += int(value)
                        else:
                            request.session['cart'][key] = int(value)
                    elif int(value) < 0:
                        if cart.get(key, 0) + int(value) > 0:
                            request.session['cart'][key] += int(value)
                        elif cart.get(key, 0):
                            del request.session['cart'][key]
                        else:
                            pass
            case _:
                return Response({'message': f'unknown action: {action}'},
                                status=status.HTTP_400_BAD_REQUEST)
        for key, value in self.request.session['cart'].items():
            if value <= 0:
                self.request.session['cart'].pop(key)
        request.session.modified = True
        return Response(
            {'message': 'cart updated'},
            status=status.HTTP_202_ACCEPTED)

    def options(self, request, *args, **kwargs):
        return Response({
            'name': 'Cart List',
            'description': 'API endpoint that allows Cart to be viewed or'
            ' edited.',
            'renders': [
                'application/json',
                'text/html'
            ],
            'parses': [
                'application/json',
            ],
            'actions': {
                'POST': {
                    'action': {
                        'type': 'string',
                        'required': True,
                        'choices': [
                            'add', 'flush', 'remove', 'update'
                        ]
                    }
                }
            },
            'examples': {
                'POST':
                    [
                        {
                            'action': 'add',
                            'mock_id_string_1': 2,
                            'mock_id_string_2': 3,
                        },
                        {
                            'action': 'flush',
                        },
                        {
                            'action': 'remove',
                            'mock_id_string_1': True,
                            'mock_id_string_2': True,
                        },
                        {
                            'action': 'update',
                            'mock_id_string_1': 2,
                            'mock_id_string_2': -3,
                        }
                    ]
                }
            })


def validate_product(pk):
    product = models.Product.objects.filter(pk=pk)
    return product.exists()
