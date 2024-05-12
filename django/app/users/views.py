import os
import requests
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json  # json 모듈을 임포트합니다.
from dotenv import load_dotenv  # dotenv 모듈을 임포트합니다.

load_dotenv()  # .env 파일을 로드합니다.

# 아라 추가
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from .serializers import MyInfoUserSerializer, UserSerializer
from django.contrib.auth.password_validation import validate_password

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

# 사용자 인증
from rest_framework.authentication import TokenAuthentication

# 권한 부여
from rest_framework.permissions import IsAuthenticated

# jwt 인증
from app.authentication import JWTAuthentication
import jwt
from django.conf import settings


class JWTLogin(APIView):
    def post(self, request):
        member_email = request.data.get("member_email")
        password = request.data.get("password")
        is_staff = request.data.get("is_staff")

        if not member_email:
            raise ParseError("email or (email and password) is required.")

        user = authenticate(
            request, member_email=member_email, password=password, is_staff=is_staff
        )

        if user:
            # jwt.encode(payload, key, algorithm)
            payload = {"memeber_id": user.member_id, "member_email": user.member_email}
            # create token
            token = jwt.encode(
                payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
            )

            return Response({"token": token})


# /users [GET, POST]
class Users(APIView):
    # permission_classes = [IsAuthenticated]  # 추가: 인증 설정

    # 전체 유저 리스트
    def get(self, request):
        users = User.objects.all()  # 객체
        # object -> json (serializer), queryset이므로 many = True is required
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 사용자 생성
    def post(self, request):
        # password 받아오기
        password = request.data.get("password")
        serializer = MyInfoUserSerializer(data=request.data)
        # Validate password if provided
        if password:
            try:
                validate_password(password)
            except:
                raise ParseError("Invalid Password")

        if serializer.is_valid():
            # Create new user object from serializer data
            user = serializer.save()

            # Set password if provided and save user
            if password:
                user.set_password(password)
                user.save()

            # Return serialized user data in response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle serializer validation errors
            raise ParseError(serializer.errors)


# /users/myinfo [GET, PUT]
class MyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MyInfoUserSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # user data update : data = request.data, partial = True
        serializer = MyInfoUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()  # user 객체 저장
            serializer = MyInfoUserSerializer(user)  # user 객체 -> json
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserDetail(APIView):

    # 특정 유저 불러오기
    def get_object(self, member_id):
        try:
            return User.objects.get(member_id=member_id)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, member_id):
        user = self.get_object(member_id=member_id)
        # serializer : object -> json
        serializer = MyInfoUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# customize authentication logic
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        is_staff = request.data.get("is_staff")
        member_email = request.data.get("member_email")
        password = request.data.get("password")

        if is_staff is None or member_email is None:
            return Response(
                {
                    "error": "Please provide email address or (email address and password)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            member_email=member_email, password=password, is_staff=is_staff
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request):
        member_email = request.data.get("member_email")
        password = request.data.get("password")
        is_staff = request.data.get("is_staff")

        if not member_email:
            raise ParseError("email or (email and password) is required.")

        user = authenticate(
            request, member_email=member_email, password=password, is_staff=is_staff
        )

        if user:
            login(request, user)  # Log in the authenticated user
            return Response({"message": "Login Success!"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Your email or password is not valid, try again!"},
                status=status.HTTP_403_FORBIDDEN,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("header : ", request.headers)
        logout(request)

        return Response({"message": "logout!"}, status=status.HTTP_200_OK)


# 대성 추가
@csrf_exempt
def check_email(request):
    if request.method == "POST":
        try:
            data = json.loads(
                request.body
            )  # request.body에서 JSON 데이터를 로드합니다.
            email = data.get("email")  # 이메일 값을 가져옵니다.
        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 데이터 형식입니다."}, status=400)

        api_key = os.getenv("EMAIL_API_KEY")
        try:
            api_response = requests.get(
                f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email={email}"
            )
            api_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"message": "API 요청에 실패했습니다."}, status=500)

        api_response_json = api_response.json()
        if api_response_json.get("status") == "valid":
            return JsonResponse({"message": "유효한 이메일입니다."})
        else:
            return JsonResponse({"message": "유효하지 않은 이메일입니다."}, status=400)

    return JsonResponse({"message": "잘못된 요청입니다."}, status=400)


@csrf_exempt
def register_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 데이터 형식입니다."}, status=400)

        if email is None:
            return JsonResponse(
                {"message": "이메일이 제공되지 않았습니다."}, status=400
            )
        if not User.objects.filter(member_email=email).exists():
            member = User(member_email=email)
            member.save()
            response = JsonResponse({"message": "이메일이 성공적으로 등록되었습니다."})
            response.set_cookie("email_registered", "true")
            response.status_code = 200
            return response
        else:
            response = JsonResponse(
                {"message": "이미 존재하는 이메일입니다."}, status=400
            )
            response.set_cookie("email_registered", "true")
            return response

    return JsonResponse({"message": "잘못된 요청입니다."}, status=400)
