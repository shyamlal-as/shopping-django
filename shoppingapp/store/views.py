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

def product(request):
	items=Product.objects.all()
	categories=Categories.objects.all()
	categoryID=request.GET.get('category')

	if categoryID:
		products=Product.get_all_products_by_categoryid(categoryID)

	else:
		products=Product.objects.all()
	data={}
	data['products']=products
	data['categories']=categories

	return render(request,'store/prod.html',data)

def category(request):
	lists=Categories.objects.all()
	return render(request,'store/first.html',{'lists':lists})