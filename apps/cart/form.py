from django import forms


class ChangeProductQuantity(forms.Form):
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'quantity-input'}))
