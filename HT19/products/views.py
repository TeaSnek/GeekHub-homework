import sys
import subprocess as sp
from typing import Any

from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView
)
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from . import models
from . import utils


class LandingTemplateView(TemplateView):
    template_name = 'products/landing.html'


class ProductsListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products_list'

    def get_queryset(self) -> QuerySet[Any]:
        return models.Product.objects.all()


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product_details'
    model = models.Product

    def post(self, request, *, sears_id, quantity):
        product = models.Product.objects.filter(sears_id=sears_id)
        if request.session.get('cart', {}):
            try:
                request.session['cart'][product] += quantity
            except KeyError:
                request.session['cart'][product] = quantity
        else:
            request.session['cart'] = {product: quantity}


class AddProductsFormView(FormView):
    template_name = 'products/add_products.html'
    form_class = utils.NewProductForm
    success_url = 'products'

    def form_valid(self, form: Any) -> HttpResponse:
        categories = form.cleaned_data['product_categories']
        curr_exec = sys.executable
        sp.Popen([
            curr_exec,
            'manage.py',
            'scrape',
            categories
        ])
        return super(AddProductsFormView, self).form_valid(form)


class CartListView(ListView):
    template_name = 'products/cart_list.html'
    context_object_name = 'cart_list'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        print(cart)
        self.object_list = {models.Product.objects.get(
            sears_id=key): quantity for key, quantity in cart.items()}
        context = self.get_context_data()
        return self.render_to_response(context)


def add_to_cart(request, ):
    data = request.POST
    quantity = int(data['quantity'])
    redir = request.POST.get('reverse', 'products:product_detail')
    if quantity > 0:
        if not request.session.get('cart', {}):
            request.session['cart'] = {data['product']: quantity}
        else:
            try:
                print(request.session['cart'])
                request.session['cart'][data['product']] += quantity
                request.session.modified = True
                print(request.session['cart'])
            except KeyError:
                request.session['cart'][data['product']] = quantity
                request.session.modified = True
    try:
        return HttpResponseRedirect(reverse(redir,
                                            args=(data['product'],)))
    except NoReverseMatch:
        return HttpResponseRedirect(reverse(redir,))


def remove_from_cart(request, ):
    data = request.POST
    quantity = int(data['quantity'])
    try:
        if not (0 < quantity <= request.session.get(
                'cart', {})[data['product']]):
            return HttpResponseRedirect(reverse('products:cart',))
    except KeyError:
        return HttpResponseRedirect(reverse('products:cart',))

    request.session['cart'][data['product']] -= quantity
    if request.session['cart'][data['product']] == 0:
        request.session['cart'].pop(data['product'], None)
    request.session.modified = True
    return HttpResponseRedirect(reverse('products:cart',))


def flush_cart(request, ):
    data = request.POST
    redir = data.get('reverse', 'products:cart')
    if request.session.get('cart', {}):
        request.session['cart'].clear()
    request.session.modified = True
    return HttpResponseRedirect(reverse(redir,))
