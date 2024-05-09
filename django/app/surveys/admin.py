from django.contrib import admin
from .models import Question, Survey, Answer

admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Answer)
