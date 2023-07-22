from django import forms
from club.models import Club, Fx


class TierForm(forms.Form):
    tiers = Club.objects.all()
    data = []
    for tier in tiers:
        data.append((tier.id, tier.tier))

    options = forms.ChoiceField(choices=data, label="Select your tier here")


class FxForm(forms.Form):
    fxs = Fx.objects.all()
    data = []
    for fx in fxs:
        data.append((fx.id, fx.fx_name))

    fx_choice = forms.ChoiceField(choices=data, label="Select your Currency here")


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16)
    card_expiry_month = forms.IntegerField(max_value=12)
    card_expiry_year = forms.IntegerField(max_value=99)
    card_expiry_cvv = forms.CharField(min_length=3, max_length=3)
