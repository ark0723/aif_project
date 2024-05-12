# import os
# import requests
# from django.http import JsonResponse
# from .models import Member
# from django.views.decorators.csrf import csrf_exempt
# import json  # json 모듈을 임포트합니다.
# from dotenv import load_dotenv  # dotenv 모듈을 임포트합니다.

# load_dotenv()  # .env 파일을 로드합니다.

# # 아라 추가
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .serializers import UserSerializer


# class Users(APIView):
#     # permission_classes = [IsAuthenticated]  # 추가: 인증 설정

#     # 전체 유저 리스트
#     def get(self, request):
#         users = Member.objects.all()  # 객체

#         # object -> json (serializer), queryset이므로 many = True is required
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # 사용자 생성
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDetail(APIView):

#     # 특정 유저 불러오기
#     def get_object(self, member_id):
#         try:
#             return Member.objects.get(member_id=member_id)
#         except Member.DoesNotExist:
#             raise NotFound

#     def get(self, request, member_id):
#         user = self.get_object(member_id=member_id)
#         # serializer : object -> json
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# # 대성 추가
# @csrf_exempt
# def check_email(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(
#                 request.body
#             )  # request.body에서 JSON 데이터를 로드합니다.
#             email = data.get("email")  # 이메일 값을 가져옵니다.
#         except json.JSONDecodeError:
#             return JsonResponse({"message": "잘못된 데이터 형식입니다."}, status=400)

#         api_key = os.getenv("EMAIL_API_KEY")
#         try:
#             api_response = requests.get(
#                 f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email={email}"
#             )
#             api_response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             return JsonResponse({"message": "API 요청에 실패했습니다."}, status=500)

#         api_response_json = api_response.json()
#         if api_response_json.get("status") == "valid":
#             return JsonResponse({"message": "유효한 이메일입니다."})
#         else:
#             return JsonResponse({"message": "유효하지 않은 이메일입니다."}, status=400)

#     return JsonResponse({"message": "잘못된 요청입니다."}, status=400)


# @csrf_exempt
# def register_email(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             email = data.get("email")
#         except json.JSONDecodeError:
#             return JsonResponse({"message": "잘못된 데이터 형식입니다."}, status=400)

#         if email is None:
#             return JsonResponse(
#                 {"message": "이메일이 제공되지 않았습니다."}, status=400
#             )
#         if not Member.objects.filter(member_email=email).exists():
#             member = Member(member_email=email)
#             member.save()
#             response = JsonResponse({"message": "이메일이 성공적으로 등록되었습니다."})
#             response.set_cookie("email_registered", "true")
#             response.status_code = 200
#             return response
#         else:
#             response = JsonResponse(
#                 {"message": "이미 존재하는 이메일입니다."}, status=400
#             )
#             response.set_cookie("email_registered", "true")
#             return response

#     return JsonResponse({"message": "잘못된 요청입니다."}, status=400)
