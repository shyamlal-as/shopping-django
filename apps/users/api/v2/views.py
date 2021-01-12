import sys 
sys.path.append("..")
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.authtoken.models import Token


from .serializers import RegistrationSerializer

from constants.messages import errors,success

@api_view(['POST',])
@authentication_classes([])
@permission_classes([])
def registration_view(request):


    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = success.REGISTRATION_SUCCESFUL
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token']=token
        else:
            data = serializer.errors
        return Response(data)