from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
    add1 = forms.CharField(label="Street Address", widget = forms.TextInput(attrs={
        'placeholder':' Downing Street '
    }))
    add2 = forms.CharField(label="Apartment Address",  widget = forms.TextInput(attrs={
        'placeholder':' Apartment 1080 '
    }))
    country = CountryField(blank_label='Choose Country').formfield(widget= CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'id':'zip',
        'class':'form-control',
    }))
    same_add = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id':'same_add'
    }), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id':'save_info'
    }), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(attrs={
        'name': 'payment_option',
    }),
        choices= PAYMENT_CHOICES)