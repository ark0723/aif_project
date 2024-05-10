from rest_framework.serializers import ModelSerializer
from .models import Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"  # 전체 필드 직렬화


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = (
            "member_email",
            "img_uuid",
            "img_generate_count",
            "auth_group",
            "created_at",
            "updated_at",
        )
