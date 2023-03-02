from django import forms


class LotForm(forms.Form):
    lot_id = forms.CharField(label='ID лоту',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ID лоту'}))
