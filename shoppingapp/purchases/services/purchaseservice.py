from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from purchases.models import shipping
from users.models import Profile
from datetime import date
from django.contrib import messages
from constants.messages import success, errors


class PurchaseService:

    product=Product.objects
    category=Categories.objects
    purchase=Purchases.objects
    productPurchase=ProductPurchases.objects

    def CreateCart(self,request,slug):

        """
        Create a cart

        :param WSGI Request request: Request object
        :param slug slug: Product id

        :return string: Success or error message
        """

        if not self.purchase.filter(Users_ID=request.user,isActive=True).exists():
            purchaseDetail=Purchases(Users_ID=request.user)
            purchaseDetail.save()
            pid=self.product.get(id=slug)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=self.purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
            message=success.CREATE_CART
        else:
            purchase=self.purchase.get(Users_ID=request.user,isActive=True)
            if not self.productPurchase.filter(product_ID=slug,purchases_ID=purchase.id).exists():
                product=self.product.get(id=slug)
                pr=product.price
                pid=self.product.get(id=slug)
                purchaseProduct=ProductPurchases(purchases_ID=purchase,product_ID=pid,quantity=1,price=pr)
                purchaseProduct.save()
                message=success.ADDED_TO_CART
            else:
                purchaseProduct=self.productPurchase.get(product_ID=slug,purchases_ID=purchase.id)
                purchaseProduct.quantity=purchaseProduct.quantity+1
                purchaseProduct.save()
                message=success.QUANTITY_INCREMENTED
        return(message)
                
                
    def DisplayCart(self,request):

        """
        Displays an html page with products in cart

        :param WSGI Request request: Request object

        :return Dictionary: Product list and amount
        """

        eq=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        products=[]
        amount=0
        if self.purchase.filter(Users_ID=request.user,isActive=True).exists():
            for each in self.productPurchase.order_by('product_ID'):
                if each.purchases_ID.id==eq.id and each.purchases_ID.isActive==True and each.purchases_ID.Users_ID==request.user:
                    products.append(each)
                    amount+=each.price*each.quantity
        context = {'products':products,'price':amount}
        return(context)


    def RemoveProduct(self, request):

        """
        Remove a product from cart

        :param WSGI Request request: Request object

        :return render: html template
        """

        idd=request.POST.get('id')
        n=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        self.productPurchase.filter(product_ID=int(idd),purchases_ID=n.id).delete()
        context=self.DisplayCart(request)
        return(context)


    def IncreaseQuantity(self, request, plus):

        """
        Increase quantity of a product in the cart

        :param WSGI Request request: Request object
        :param slug plus: Product id

        :return render: html template
        """
        
        n=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        quantity=self.productPurchase.get(product_ID=int(plus),purchases_ID=n.id)
        prod=Product.objects.get(id=plus)
        if quantity.quantity<prod.stock:
            newquantity=quantity.quantity+1
            quantity.quantity=newquantity
            quantity.save()
        else:
            message=errors.QUANTITY_EXCEEDED
            messages.success(request,  message)
        context=self.DisplayCart(request)
        return(context)


    
    def DecreaseQuantity(self, request,minus):

        """
        Increase quantity of a product in the cart

        :param WSGI Request request: Request object
        :param slug plus: Product id

        :return render: html template
        """
        
        n=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        quantity=self.productPurchase.get(product_ID=int(minus),purchases_ID=n.id)
        if(quantity.quantity == 1):
            self.RemoveProduct(request)
        else:
            newquantity=quantity.quantity-1
            quantity.quantity=newquantity
            quantity.save()
        context=self.DisplayCart(request)
        return(context)


    def Checkout(self, request):

        """
        Checkout the current cart

        :param WSGI Request request: Request object

        :return render: html template
        """

        n=Purchases.objects.filter(Users_ID=request.user,isActive=True).first()
        for each in ProductPurchases.objects.filter(purchases_ID=n.id):
            if each.quantity<=each.product_ID.stock:
                q=each.quantity
                each.product_ID.stock-=q
                each.product_ID.save()

                n.isActive=False
                n.save()
                address=request.GET.get('address')
                city=request.GET.get('city')
                pincode=request.GET.get('pincode')
                shippingdets=shipping(Users_ID=request.user,address=address,city=city,pincode=pincode)
                shippingdets.save()
            else:
                for each in self.productPurchase.filter(purchases_ID=n.id):
                    if each.quantity > each.product_ID.stock:
                        diff= each.quantity-each.product_ID.stock
                        for i in range(int(diff)):
                            self.DecreaseQuantity(request,each.product_ID.id)
                            


    
    def ClearCart(self, request):

        """
        Clear all products in the cart

        :param WSGI Request request: Request object

        :return render: html template
        """
        
        purchase=request.GET.get('purchaseID')
        self.purchase.filter(id=purchase).delete()