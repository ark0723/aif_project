from django.urls import path
from . import views

urlpatterns = [
    path("", views.Questions.as_view()),
    path("<int:question_id>", views.QuestionDetail.as_view()),
    path("answer/<int:member_id>", views.AnswersByUser.as_view()),
]
