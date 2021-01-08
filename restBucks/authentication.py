import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings

from user.models import User


class SafeJWTAuthentication(BaseAuthentication):
    """
        custom authentication class for DRF and JWT
       https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    """

    def authenticate(self, request):
        access_token = request.headers.get('Authorization')

        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        return user, None

