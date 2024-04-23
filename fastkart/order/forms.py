from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name","phone", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name","class":"form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone","class":"form-control"}),
            "address": forms.Textarea(attrs={"placeholder": "Enter Your Comments" , "rows": 3,"class":"form-control"}),
        }
    
    