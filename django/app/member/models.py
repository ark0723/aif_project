# from django.db import models
# from common.models import CommonModel
# import uuid
# from datetime import timedelta
# from django.utils import timezone


# class Member(CommonModel):
#     GROUP_CHOICESE = [
#         ("general", "일반"),  # (DB에 저장할 실제 값, display 값)
#         ("staff", "스태프"),
#         ("admin", "관리자"),
#     ]
#     member_id = models.AutoField(primary_key=True)
#     member_email = models.EmailField(max_length=100, unique=True, null=False)
#     member_password = models.CharField(max_length=255, null=True)
#     img_uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False)
#     img_generate_count = models.PositiveSmallIntegerField(default=0)
#     auth_group = models.CharField(
#         max_length=10, choices=GROUP_CHOICESE, default="general"
#     )
#     is_admin = models.BooleanField(default=False)
#     mem_waiting = models.BooleanField(default=False)  # 승인대기
#     mem_number = models.CharField(max_length=20, null=True)  # 전화번호

#     def __str__(self):
#         return f"{self.member_email} / {self.is_admin}"


# class Image(CommonModel):
#     img_id = models.AutoField(primary_key=True)
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     img_url = models.CharField(max_length=255)
#     keyword_input = models.TextField()
#     generating_count = models.SmallIntegerField(default=0)
#     style_code = models.CharField(max_length=20)
#     expiration_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))

#     def __str__(self):
#         return f"ID: {self.img_id}, Member: {self.member}, keyword: {self.keyword_input}, style: {self.style_code}, URL: {self.img_url}"


# class RefreshToken(CommonModel):
#     refresh_token_id = models.CharField(
#         max_length=255, primary_key=True, default=uuid.uuid4, editable=False
#     )
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     expiration_date = models.DateTimeField()

#     @classmethod
#     def create(cls, member):
#         # Generate a new refresh token instance
#         refresh_token = cls(member=member)
#         refresh_token.set_expiration()
#         refresh_token.save()
#         return refresh_token

#     def set_expiration(self):
#         # Set the expiration date for the refresh token (e.g., 30 days from now)
#         self.expiration_date = timezone.now() + timedelta(days=30)

#     def is_expired(self):
#         # Check if the refresh token has expired
#         return self.expiration_date < timezone.now()
