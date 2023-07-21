from django import forms
from carapp.models import OrderVehicle

class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'quantity']
        labels = {
            'vehicle': 'Vehicle',
            'buyer': 'Buyer',
            'quantity': 'Number of Vehicles Ordered'
        }
        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))