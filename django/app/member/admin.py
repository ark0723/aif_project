from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # display fields
    list_display = [
        "member_email",
        "img_uuid",
        "img_generate_count",
        "auth_group",
        "is_admin",
        "mem_waiting",
        "created_at",
    ]
    # add filter
    list_filter = ["auth_group", "mem_waiting"]
    # search field
    search_fields = ["member_email", "img_uuid"]
    # created_at descending order
    ordering = ("-created_at",)
    readonly_fields = ("member_email", "img_generate_count", "auth_group", "is_admin")
    # pagination
    list_per_page = 10
    # add action
    actions = ("approval",)

    def approval(self, request, queryset):
        # 선택된 게시글들에 대해 'likes' 수를 1씩 증가
        for member in queryset:
            member.mem_waiting = False
            member.save()

    approval.short_description = "staff 가입 승인"
