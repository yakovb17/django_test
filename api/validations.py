from django import forms


class NewUrlValidation(forms.Form):
    url = forms.URLField(required=True)
