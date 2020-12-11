from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from users.forms import RegistrationForm,UserAuthenticationForm

from django.contrib import messages


# Create your views here.


def registration_view(request):
    context={}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password= raw_password)
            login(request, account)
            return redirect('store')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html',context)
    


def logout_view(request):
    #logout(request)
    #return redirect('store')
    if request.method=='POST':
        logout(request)
        messages.success(request,  'Logged Out.')
        return render(request,'store/store.html')
    else:
        return render(request,'users/profile.html')



def login_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        return redirect('store')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)

            if user:
                login(request, user)
                return redirect('store')

    else:
        form = UserAuthenticationForm()    
    context['login_form'] = form
    return render(request, 'users/login.html',context)