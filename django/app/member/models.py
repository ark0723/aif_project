from django.db import models
from common.models import CommonModel


class Member(CommonModel):
    member_id = models.PositiveIntegerField(primary_key=True)
    member_email = models.EmailField(max_length=100, unique=True, null=False)
    member_password = models.CharField(max_length=255)
    img_uuid = models.CharField(max_length=255)
    img_generate_count = models.PositiveSmallIntegerField(default=0)
    auth_group = models.CharField(max_length=20)  # 선택가능하게
    is_admin = models.BooleanField(default=False)
    mem_waiting = models.BooleanField(default=False)
    mem_number = models.CharField(max_length=20)
