from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from store.models import Product
from api.v1.store.serializers import ProductSerializer, CategorySerializer

from services import responseservices
from constants.messages import success,errors

#from store.returns import api_return

## Get Product

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_product_view(request,slug):


    try:
        product= Product.objects.get(id=slug)
    except Product.DoesNotExist:
        message = errors.PRODUCT_ERROR
        #message='A product of the requested id does not exist'
        obj=responseservices.ResponseServices(message)
        return Response(obj.NotFound(), status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)



## Get Category


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_category_view(request,slug):


    try:
        product= Product.objects.filter(categories_id=slug)
    except Product.DoesNotExist:
        #message='A product of the requested category id does not exist'
        message=errors.CATEGORY_ERROR
        obj=responseservices.ResponseServices(message)
        return Response(obj.NotFound(), status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "GET":
        products=[]
        for each in product:
            products.append(each)
        serializer = CategorySerializer(products, many=True)
       
        return Response(serializer.data, status.HTTP_200_OK)


##############################################################################

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def product_api(request):
    return Response("worked",status.HTTP_200_OK)