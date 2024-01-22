import sys
import subprocess as sp
from typing import Any

from django.contrib.auth import (
    logout,
)
from django.contrib.auth.views import (
    LoginView,
)
from django.db.models.query import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
)
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from . import models
from . import utils


class LandingTemplateView(TemplateView):
    template_name = 'products/landing.html'

    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponseRedirect(reverse('products:products_list'),)


class ProductsListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products_list'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.update({
            'categories': models.Category.objects.all(),
            'current': self.kwargs.get('category', 'All')
            })
        return super().get_context_data(**kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return models.Product.objects.filter(
            category=self.kwargs.get('category', 'All')
        )


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


class EditProductFormView(FormView):
    template_name = 'products/edit.html'
    form_class = utils.EditProductForm
    context_object_name = 'product_details'

    def get_success_url(self) -> str:
        return reverse('products:product_detail',
                       kwargs={'pk': self.kwargs.get('pk', '')})

    def get_context_data(self, **kwargs):
        context = super(EditProductFormView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', '')
        if pk:
            context['product_details'] = models.Product.objects.get(pk=pk)
        return context

    def get_initial(self):
        pk = self.kwargs.get('pk', '')
        initial = super().get_initial()
        if pk:
            product = models.Product.objects.get(pk=pk)
            initial['product_name'] = product.product_name
            initial['price'] = product.price
            initial['short_about'] = product.short_about
            initial['brand'] = product.brand
            initial['category'] = product.category.all()
            initial['sears_link'] = product.sears_link
        return initial

    def form_valid(self, form: Any) -> HttpResponse:
        if form.changed_data:
            product = models.Product.objects.get(pk=self.kwargs.get('pk', ''))
            for fieldname in form.changed_data:
                if fieldname == 'category':
                    product.category.set(form.cleaned_data[fieldname])
                    continue
                setattr(product, fieldname, form.cleaned_data[fieldname])
            product.save()
        return super().form_valid(form)


class LoginFormView(LoginView):
    template_name = 'products/login.html'
    next_page = 'products:landing'


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


def logout_view(request):
    data = request.POST
    redir = data.get('reverse', 'products:landing')
    logout(request)
    return HttpResponseRedirect(reverse(redir))


def update(request):
    data = request.POST
    redir = data.get('reverse',)
    curr_exec = sys.executable
    sp.Popen([
        curr_exec,
        'manage.py',
        'scrape',
        data.get('product', '')
    ])
    return HttpResponseRedirect(redir)


def delete_view(request):
    data = request.POST
    redir = data.get('reverse', )
    if data.get('product', ''):
        product = models.Product.objects.get(pk=data['product'])
        product.delete()
    return HttpResponseRedirect(redir)
