from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


def generate_access_token(member_email):
    User = get_user_model()
    try:
        user = User.objects.get(member_email=member_email)  # Retrieve user based on ID
        access_token = AccessToken.for_user(user)  # Generate access token
        return str(access_token)  # Return the access token as a string
    except User.DoesNotExist:
        return None  # Handle user not found error


def generate_access_token_with_password(member_email, password):
    # Authenticate user
    user = authenticate(member_email=member_email, password=password, is_staff=True)

    if user is not None:
        access_token = AccessToken.for_user(user)  # Generate access token
        return str(access_token)  # Return the access token as a string
    else:
        return None  # Handle authentication failure


from django.http import JsonResponse


def get_access_token(request, member_email: str, password: str, is_staff: bool = False):
    if not is_staff:
        access_token = generate_access_token(member_email=member_email)

    access_token = generate_access_token_with_password(
        member_email=member_email, password=password
    )

    if access_token:
        return JsonResponse({"access_token": access_token})
    else:
        return JsonResponse({"error": "User not found"}, status=404)
