from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User


class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(help_text='Enter your name')
    email=forms.EmailField(help_text='Add a valid address')

    class Meta:
        model=User
        fields =('email','first_name','username','password1','password2')
        


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")