import os
import requests
from django.http import JsonResponse
from .models import Member
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def check_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        api_key = "00f1f011058d4e6a931e0f7dac18832c"
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
        email = request.POST.get("email")
        if email is None:
            return JsonResponse(
                {"message": "이메일이 제공되지 않았습니다."}, status=400
            )
        if not Member.objects.filter(member_email=email).exists():
            member = Member(member_email=email)
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
