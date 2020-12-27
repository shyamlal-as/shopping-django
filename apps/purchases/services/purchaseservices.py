from purchases.models import Purchases, ProductPurchases
from store.models import Product, Categories
from purchases.models import shipping
from users.models import Profile
from datetime import date
from django.contrib import messages


class PurchaseServices:

    product=Product.objects
    category=Categories.objects
    purchase=Purchases.objects
    productPurchase=ProductPurchases.objects

    def CreateCart(self,request,slug):
        """
        Creating a new cart or appending to existing cart
        :param WSGI request - request
        :param self- instance of class ProductServices
        :param slug- ID of product to be added into the cart

        :return message: Message indicating the inclusion of the product in the cart
        """

        if not self.purchase.filter(Users_ID=request.user,isActive=True).exists():
            purchaseDetail=Purchases(Users_ID=request.user)
            purchaseDetail.save()
            pid=self.product.get(id=slug)
            pr=pid.price
            purchaseProduct=ProductPurchases(purchases_ID=self.purchase.latest('pk'),product_ID=pid,quantity=1,price=pr)
            purchaseProduct.save()
            message='A cart has been created'
        else:
            purchase=self.purchase.get(Users_ID=request.user,isActive=True)
            if not self.productPurchase.filter(product_ID=slug,purchases_ID=purchase.id).exists():
                product=self.product.get(id=slug)
                pr=product.price
                pid=self.product.get(id=slug)
                purchaseProduct=ProductPurchases(purchases_ID=purchase,product_ID=pid,quantity=1,price=pr)
                purchaseProduct.save()
                message='Product was added to the cart'
            else:
                purchaseProduct=self.productPurchase.get(product_ID=slug,purchases_ID=purchase.id)
                purchaseProduct.quantity=purchaseProduct.quantity+1
                purchaseProduct.save()
                message='Quantity of the product increased by one'
        return(message)
                
                
    def DisplayCart(self,request):
        """
        Displaying the cart 

        :param WSGI request - request
        :param self- instance of class ProductServices

        :return dictionary context : A dictionary containing the products in the cart
                                     and the total price of all products summed up
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
        Removing a prodcut from the cart
        :param WSGI request - request
        :param self- instance of class ProductServices

         :return dictionary context : A dictionary containing the products in the cart
                                     and the total price of all products summed up
        """
        idd=request.POST.get('id')
        n=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        self.productPurchase.filter(product_ID=int(idd),purchases_ID=n.id).delete()
        context=self.DisplayCart(request)
        return(context)


    def IncreaseQuantity(self, request, plus):
        """
        Increasing quantity of selected product
        :param WSGI request - request
        :param self- instance of class ProductServices
        :param plus- ID of the product

         :return dictionary context : A dictionary containing the products in the cart
                                     and the total price of all products summed up
        """
        
        n=self.purchase.filter(Users_ID=request.user,isActive=True).first()
        quantity=self.productPurchase.get(product_ID=int(plus),purchases_ID=n.id)
        prod=Product.objects.get(id=plus)
        if quantity.quantity<prod.stock:
            newquantity=quantity.quantity+1
            quantity.quantity=newquantity
            quantity.save()
        else:
            messages.success(request,  'Quantity exceeded product stock.')
        context=self.DisplayCart(request)
        return(context)


    
    def DecreaseQuantity(self, request,minus):
        """
        Decreasing quantity of selected product
        :param WSGI request - request
        :param self- instance of class ProductServices
        :param minus- ID of the product

         :return dictionary context : A dictionary containing the products in the cart
                                     and the total price of all products summed up
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
        Completing the purchase
        :param WSGI request - request
        :param self- instance of class ProductServices
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
                print("---------------------------------------Unsuccesfull-------------------")
                for each in self.productPurchase.filter(purchases_ID=n.id):
                    if each.quantity > each.product_ID.stock:
                        diff= each.quantity-each.product_ID.stock
                        for i in range(int(diff)):
                            self.DecreaseQuantity(request,each.product_ID.id)
                            


    
    def ClearCart(self, request):
        """
        Deleting all the products from the cart
        :param WSGI request - request
        :param self- instance of class ProductServices
        """
        purchase=request.GET.get('purchaseID')
        PurchaseServices().purchase.filter(id=purchase).delete()