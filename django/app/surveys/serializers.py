from rest_framework.serializers import ModelSerializer
from .models import Question, Answer
from member.serializers import UserAnswerSerializer


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"  # 전체 필드 직렬화


class AnswerSerializer(ModelSerializer):
    user = UserAnswerSerializer()

    class Meta:
        model = Answer
        fields = "__all__"
        depth = 1
