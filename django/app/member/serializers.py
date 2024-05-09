from rest_framework.serializers import ModelSerializer
from .models import Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"  # 전체 필드 직렬화

        # depth = 1
