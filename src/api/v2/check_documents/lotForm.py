from django import forms


class LotForm(forms.Form):
    lot_id = forms.CharField(label='ID лоту',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ID лоту, в форматі :70a0c7e7289b4c4eae86e691b3b46c8c'}))
