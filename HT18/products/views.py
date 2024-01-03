import sys
import subprocess as sp
from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView
)

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
