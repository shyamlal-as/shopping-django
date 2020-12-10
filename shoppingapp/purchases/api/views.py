from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from purchases.models import Purchases, ProductPurchases
from store.models import Product


from purchases.api.serializers import PurchaseSerializer, AddToCartSerializer, ConfirmPurchaseSerializer


#Create Cart

@api_view(['POST',])
def cart_api_view(request,slug):

    purchases = Purchases(Users_ID= request.user)
    

    if request.method == 'POST':
        serializer = PurchaseSerializer(purchases, data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            propurchasefn(request,slug)
            data={'message':'Cart Created'}
            return Response(data)


def propurchasefn(request,slug):
    product = Product.objects.filter(id=slug).first()
    propurchases = ProductPurchases(purchases_ID= Purchases.objects.latest('pk'), 
    product_ID=product,
    price=product.price,quantity=1)
    serializer = AddToCartSerializer(propurchases, data=request.data)
    data={}
    if serializer.is_valid():
        user=serializer.save()
        data['purch']=' success'
        return Response(data)



# Purchase cart


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def cart_purchase_api(request,slug):


    try:
        purchase = Purchases.objects.get(Users_ID=request.user, isActive=True)
    except Purchases.DoesNotExist:
        data={}
        data['message']='No product on this id'
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "PUT":
        #propurchases = purchase(isActive=False, Users_ID=request.user)
        dat={}
        #dat['isActive']=False
        serializer = ConfirmPurchaseSerializer(purchase, data=request.data)
        print('----------------------------------------')
        print(request.data)
        print('------------------------------')
        data={}
        if serializer.is_valid():
            serializer.save()
            data['success']='Update Succesful'
            return Response(data=data)
        return Response(serializer.errors, status.HTTP_200_OK)