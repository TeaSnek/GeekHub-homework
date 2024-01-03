from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


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
