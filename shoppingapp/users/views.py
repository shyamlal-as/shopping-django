from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import RegistrationForm,UserAuthenticationForm,UserUpdateForm

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
            messages.success(request,  'Signed Up.')
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
        #messages.success(request,  'Logged Out.')
        return redirect('store')
    else:
        return render(request,'users/profile.html')


def login_view(request):
    context= {}
    user = request.user

    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)

            if user:
                login(request, user)
                messages.success(request,  'Logged In.')
                return redirect('store')

    else:
        form = UserAuthenticationForm()    
    context['login_form'] = form
    return render(request, 'users/login.html',context)


def user_view(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    context={}

    if request.POST:
        form = UserUpdateForm(request.POST, instance=request.user)
        form.save()

    else:
        form = UserUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
                'firstname':request.user.first_name
            }
        )

    context['account_form']=form
    return render(request, 'store/edit_profile.html',context)