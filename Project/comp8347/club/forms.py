from django import forms
from club.models import Club


class TierForm(forms.Form):
    tiers = Club.objects.all()
    data = []
    for tier in tiers:
        data.append((tier.id, tier.tier))
    options = forms.ChoiceField(choices=data, label="Select you tier here")

