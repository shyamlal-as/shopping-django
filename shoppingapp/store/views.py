from django.shortcuts import render
from .models import Categories,Product

# Create your views here.

def store(request):
	products=Product.objects.all()
	context={}
	return render(request,'store/store.html',{'products':products})

def cart(request):
	context={}
	return render(request,'store/cart.html',context)

def checkout(request):
	context={}
	return render(request,'store/checkout.html',context)

def product(request,categories_id):
	products=Product.objects.filter(categories_id=categories_id)
	return render(request,'store/prod.html',{'products':products})

def category(request):
	lists=Categories.objects.all()
	return render(request,'store/first.html',{'lists':lists})