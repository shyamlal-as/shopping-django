from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User


class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(help_text='Enter your name',widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    email=forms.EmailField(help_text='Add a valid address',widget=forms.TextInput(attrs={'placeholder':'Enter Valid Email'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re Enter Password'}))


    class Meta:
        model=User
        fields =('email','first_name','username','password1','password2')
        


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    email = forms.CharField(label='email',widget=forms.TextInput)


    class Meta:
        model = User
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username','first_name')


    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % user)
            

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % user.username)

