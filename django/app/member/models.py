from django.db import models
from common.models import CommonModel
import uuid
from datetime import timedelta
from django.utils import timezone


class Member(CommonModel):
    GROUP_CHOICESE = [
        ("general", "일반"),  # (DB에 저장할 실제 값, display 값)
        ("staff", "스태프"),
        ("admin", "관리자"),
    ]
    member_id = models.PositiveIntegerField(primary_key=True)
    member_email = models.EmailField(max_length=100, unique=True, null=False)
    member_password = models.CharField(max_length=255)
    img_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    img_generate_count = models.PositiveSmallIntegerField(default=0)
    auth_group = models.CharField(
        max_length=10, choices=GROUP_CHOICESE, default="general"
    )
    is_admin = models.BooleanField(default=False)
    mem_waiting = models.BooleanField(default=False)  # 승인대기
    mem_number = models.CharField(max_length=20)  # 전화번호


class RefreshToken(CommonModel):
    refresh_token_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()

    @classmethod
    def create(cls, member):
        # Generate a new refresh token instance
        refresh_token = cls(member=member)
        refresh_token.set_expiration()
        refresh_token.save()
        return refresh_token

    def set_expiration(self):
        # Set the expiration date for the refresh token (e.g., 30 days from now)
        self.expiration_date = timezone.now() + timedelta(days=30)

    def is_expired(self):
        # Check if the refresh token has expired
        return self.expiration_date < timezone.now()
