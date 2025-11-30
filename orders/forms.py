from django import forms
from django.shortcuts import redirect
from .models import Order, Orderpayment
from django.forms import ModelForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'email','city' , 'address']
        
        
        
class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Orderpayment
        fields = ['pay_phone', 'pay_image']
        
    def clean_pay_phone(self):
        pay_phone = self.cleaned_data.get('pay_phone')
        if not pay_phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(pay_phone) != 11:
            raise forms.ValidationError("Phone number must be  11.")
        
        valid_prefixes = ['010', '011', '012', '015']
        if not any(pay_phone.startswith(prefix) for prefix in valid_prefixes):
            raise forms.ValidationError("Phone number must start with a valid prefix (010, 011, 012, 015).")
        return pay_phone
    

