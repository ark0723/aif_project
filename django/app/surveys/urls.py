from django.urls import path
from . import views

urlpatterns = [
    path("", views.Questions.as_view()),
    path("<int:question_id>", views.QuestionDetail.as_view()),
    path("answers", views.Answers.as_view()),
    path("answer-by-user/<int:member_id>", views.AnswersByUser.as_view()),
    path("answer-by-question/<int:question_id>", views.AnswersByQuestion.as_view()),
]
