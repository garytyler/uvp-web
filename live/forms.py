from django import forms


class GuestSignUpForm(forms.Form):
    guest_name = forms.CharField(label="Your name", max_length=100)
