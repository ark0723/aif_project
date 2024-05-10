from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, Member
from .survey_forms import AnswerForm


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer, AnswerSerializer


class Questions(APIView):
    # permission_classes = [IsAuthenticated]  # 추가: 인증 설정

    # 전체 질문 리스트
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDetail(APIView):

    # 특정 질문 불러오기
    def get_question(self, question_id):
        try:
            return Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            raise NotFound

    def get(self, request, question_id):
        question = self.get_question(question_id=question_id)
        # serializer : object -> json
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 사용자 생성
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswersByUser(APIView):
    # 특정 유저가 한 모든 질문 불러오기
    def get_answers_by_user(self, member_id):
        try:
            user = Member.objects.get(member_id=member_id)

        except Member.DoesNotExist:
            raise NotFound

        return Answer.objects.filter(user=Member.objects.get(member_id=member_id))

    # /surveys/answer/<int:member_id>
    def get(self, request, member_id):
        answers = self.get_answers_by_user(member_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /surveys/answer/<int:member_id>
    def post(self, request, member_id):

        serializer = AnswerSerializer(data=request.data)
