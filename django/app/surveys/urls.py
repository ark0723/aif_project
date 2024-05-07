from django.urls import path
from . import views

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path("survey/<int:pk>/", views.survey_detail, name="survey_detail"),
    path("answer/<int:pk>/", views.save_survey_answer, name="save_survey_answer"),
]
