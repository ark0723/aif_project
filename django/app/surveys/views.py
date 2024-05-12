from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, User
from .survey_forms import AnswerForm


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer, AnswerSerializer
from users.serializers import UserAnswerSerializer


class Questions(APIView):
    # permission_classes = [IsAuthenticated]  # 추가: 인증 설정

    # 전체 질문 리스트
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 질문 생성
    def post(self, request):
        # jsont -> object
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):

    # 특정 질문 불러오기
    def get_question(self, question_id):
        try:
            return Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            raise NotFound

    # 특정 질문과 질문에 대한 답변들 불러오기
    def get(self, request, question_id):
        question = self.get_question(question_id=question_id)
        # serializer : object -> json
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /surveys/<int:question_id>

    def post(self, request, question_id):

        question = self.get_question(question_id=question_id)
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            answer = serializer.save(user=request.user, question=question)
            # Serialize the created Answer and return as response
            serializer = AnswerSerializer(answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /surveys/answers
class Answers(APIView):
    # 모든 답변 불러오기
    def get(self, request):
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)

        return Response(serializer.data)


class AnswersByUser(APIView):
    # 특정 유저가 한 모든 질문 불러오기
    def get_answers_by_user(self, member_id):
        try:
            user = User.objects.get(member_id=member_id)

        except User.DoesNotExist:
            raise NotFound

        return Answer.objects.filter(user=User.objects.get(member_id=member_id))

    # /surveys/answer-by-user/<int:member_id>
    def get(self, request, member_id):
        answers = self.get_answers_by_user(member_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswersByQuestion(APIView):

    def get_answers_by_question(self, question_id):
        try:
            question = Question.objects.get(question_id=question_id)

        except question.DoesNotExist:
            raise NotFound

        return Answer.objects.filter(
            question=Question.objects.get(question_id=question_id)
        )

    # /surveys/answer-by-question/<int:question_id>
    def get(self, request, question_id):
        # 특정 질문에 대한 answers 모두 불러오기
        answers = self.get_answers_by_question(question_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /surveys/answer-by-question/<int:question_id>
    def post(self, request, question_id):

        question = Question.objects.get(question_id=question_id)
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            answer = serializer.save(user=request.user, question=question)
            # Serialize the created Answer and return as response
            serializer = AnswerSerializer(answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
