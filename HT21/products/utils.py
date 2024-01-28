from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from . import models


def validate_noalpha(value: str):
    if any([not (char.isalpha() or char.isdecimal() or char == ' ')
            for char in value]):
        raise ValidationError(
            gettext_lazy("%(value)s must contain "
                         "only decimals or letters or whitespaces"),
            params={"value": value},
        )


class NewProductForm(forms.Form):
    product_categories = forms.CharField(
        label='Products',
        help_text='Input products separated by whitespace',
        initial='a119106373',
        required=True,
        validators=[validate_noalpha]
    )


class EditProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        required_fields = ['product_name', 'price']
        fields = ['product_name', 'price', 'short_about',
                  'brand', 'sears_link', 'category']

    category = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
