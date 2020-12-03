
from django.shortcuts import render
from .models import Categories,Product

# Create your views here.

def store(request):
	lists=Categories.objects.all()
	context={}
	return render(request,'store/store.html',{'lists':lists})

def cart(request):
	context={}
	return render(request,'store/cart.html',context)

def checkout(request):
	context={}
	return render(request,'store/checkout.html',context)

def product(request, slug):
	items=Product.objects.filter(categories_id=slug)
	return render(request,'store/index.html',{'items':items})

def category(request):
	lists=Categories.objects.all()
	return render(request,'store/first.html',{'lists':lists})

def Home(request):
    context={}
    return render(request,'store/base.html',context)

