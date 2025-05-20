import sys
import subprocess as sp
from typing import Any

from django.contrib.auth.decorators import (
    user_passes_test,
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

from . import models
from . import utils
from scraper.tasks import scrape_prod


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


class AddProductsFormView(utils.SuperUserRequiredMixin, FormView):
    template_name = 'products/add_products.html'
    form_class = utils.NewProductForm
    success_url = 'products'

    def form_valid(self, form: Any) -> HttpResponse:
        categories = form.cleaned_data['product_categories']
        scrape_prod.delay(categories.split())
        return super(AddProductsFormView, self).form_valid(form)


class EditProductFormView(utils.SuperUserRequiredMixin, FormView):
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
            initial['image'] = product.image
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


@user_passes_test(lambda u: u.is_superuser)
def delete_view(request):
    data = request.POST
    redir = data.get('reverse')
    if data.get('product', ''):
        product = models.Product.objects.get(pk=data['product'])
        product.delete()
    return HttpResponseRedirect(redir)


@user_passes_test(lambda u: u.is_superuser)
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
