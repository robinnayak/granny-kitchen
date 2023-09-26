from django import forms
from customer.models import Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number','address','profile']
        exclude = ['user','email']


