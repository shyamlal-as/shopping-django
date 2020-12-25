from django.shortcuts import render, redirect
from .models import Purchases, ProductPurchases
from store.models import Product
from django.contrib import messages

from django.db.models import Q

