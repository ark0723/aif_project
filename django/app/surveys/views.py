from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, Answer
from .survey_forms import AnswerForm


def survey_list(request):
    # 활성화된 설문들만 조회
    surveys = Survey.objects.filter(is_active=True)
    return render(request, "surveys/list.html", {"surveys": surveys})


def survey_detail(request, survey_id):
    # 주어진 survey_id로 설문 조회, 없으면 404 반환
    survey = get_object_or_404(Survey, pk=survey_id)
    form = AnswerForm()
    return render(request, "surveys/detail.html", {"survey": survey, "form": form})


def save_survey_answer(request, question_id):
    # 주어진 question_id로 질문 조회, 없으면 404 반환
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect(
                "survey_detail", survey_id=question.survey.pk
            )  # 설문 상세 페이지로 리다이렉트
    # POST가 아니거나 유효하지 않은 경우 다시 질문 상세 페이지로 리다이렉트
    return redirect("survey_detail", survey_id=question.survey.pk)


def index(request):
    return render(request, "surveys/index.html")
