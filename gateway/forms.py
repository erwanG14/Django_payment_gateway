from django import forms
from django.core.validators import MinLengthValidator

class PaiementForm(forms.Form):
    bank = forms.CharField(
        label="bank",
        max_length=10,
        validators=[MinLengthValidator(1)]
    )
    name = forms.CharField(
        label="name",
        max_length=20,
        validators=[MinLengthValidator(1)]
    )
    surname = forms.CharField(
        label="surname",
        max_length=20,
        validators=[MinLengthValidator(1)]
    )
    card_data = forms.CharField(
        label="card_data",
        min_length=12,
    )