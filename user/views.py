from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .utils import generate_access_token
from .serializers import LoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
@authentication_classes([])
def get_token(request):
    """
        this view is for getting the token for user, the token will be expired after a day
        Return access_token and user detail
        ---
        parameters:
            - name: email
              required: true
              type: string

            - name: password
              required: true
              type: string
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        password = serializer.data['password']
        user = authenticate(email=email, password=password)

        if user:
            serialized_user = UserSerializer(user)
            access_token = generate_access_token(user)
            return Response({'result': 'OK', 'data': {'access_token': access_token, 'user': serialized_user.data}},
                            status=status.HTTP_200_OK)

        else:
            return Response({'result': 'error', 'data': 'Unable to login with provided credentials.'},
                            status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

