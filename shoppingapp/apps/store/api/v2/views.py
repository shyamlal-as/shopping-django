from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from apps.store.models import Product
from .serializers import ProductSerializer, CategorySerializer

from apps.store.services import responseservice


#from store.returns import api_return

## Get Product


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_product_view(request,slug):


    try:
        product= Product.objects.get(id=slug)
    except Product.DoesNotExist:
        data={}
        data['message']='No product on this id'
        #data={'status':'success',
        #'status-code':status.HTTP_200_OK,
        #'message':'Not Found'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
        #return api_return('Success',status.HTTP_200_OK,'Not Found','This message was not found')

    
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
        message='A product of the requested category id does not exist'
        obj=responseservices.ResponseService(message)
        return Response(obj.NotFound(), status=status.HTTP_404_NOT_FOUND)

    
    if request.method == "GET":
        products=[]
        for each in product:
            products.append(each)
        serializer = CategorySerializer(products, many=True)
       
        return Response(serializer.data, status.HTTP_200_OK)