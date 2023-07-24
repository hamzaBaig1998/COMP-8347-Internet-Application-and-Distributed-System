from django import forms
from club.models import Club, Fx


class TierForm(forms.Form):
    tiers = Club.objects.all()
    data = []
    for tier in tiers:
        data.append((tier.id, tier.tier))

    options = forms.ChoiceField(
        choices=data,
        label="Select your tier here",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class FxForm(forms.Form):
    fxs = Fx.objects.all()
    data = []
    for fx in fxs:
        data.append((fx.id, fx.fx_name))

    fx_choice = forms.ChoiceField(
        choices=data,
        label="Select your Currency here",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    card_expiry_month = forms.IntegerField(
        max_value=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    card_expiry_year = forms.IntegerField(
        max_value=99,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    card_expiry_cvv = forms.CharField(
        min_length=3,
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
