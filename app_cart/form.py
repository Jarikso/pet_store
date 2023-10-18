from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1,
                                  widget=forms.TextInput(attrs={'class': 'form-input Amount-input'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
