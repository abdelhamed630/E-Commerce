from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your code",
            "class": "form-control"
        })
    )
