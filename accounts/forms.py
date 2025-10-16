from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    # username will be derived from email; make it optional and hidden in the form
    username = forms.CharField(required=False, widget=forms.HiddenInput)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    company = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "company", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        # Let UserCreationForm create the user and set the password
        user = super().save(commit=False)
        # normalize email and use it as username
        email = self.cleaned_data.get('email')
        if email:
            email_clean = email.strip().lower()
            user.email = email_clean
            user.username = email_clean
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
