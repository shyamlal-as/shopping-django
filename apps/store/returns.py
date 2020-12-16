from rest_framework.response import Response
from rest_framework import status


def api_return(_status,_statusCode,_message,_body):
    
    data={'status':_status,
        'status-code':_statusCode,
        'message':_message,
        'body':_body}

    return Response(data, status.HTTP_404_NOT_FOUND)