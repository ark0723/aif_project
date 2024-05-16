from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
import jwt
import urllib.parse  # For URL decoding


class JWTAuthentication(BaseAuthentication):
    # authenticate(): return a tuple of (user, token)
    # jwt: contains (header, payload, signature)
    def authenticate(self, request):
        token = self.get_authorization_header(request)

        if not token:  # no token
            return None

        # decode token : jwt, key, algorithms
        try:
            # Decode the token if it's URL-encoded
            token = urllib.parse.unquote(token)
            # Check for the 'Bearer' prefix and extract the token
            prefix, token = token.split()
            if prefix != "Bearer":
                raise exceptions.AuthenticationFailed("Invalid token prefix")

            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print("decoded", decoded)
            user_email = decoded.get("member_email")
            if not user_email:
                raise AuthenticationFailed("Invalid Token")

            user = User.objects.get(member_email=user_email)

            # return (user, token)
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Error decoding token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

    def get_authorization_header(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return None
        return auth_header
