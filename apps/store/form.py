from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=("name","desc","stock","categories_id","price","image","User_ID")
        