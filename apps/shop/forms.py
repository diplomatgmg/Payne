from django import forms


class SearchProductsForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))
