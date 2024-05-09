from django.db import models
from member.models import Member


class Question(models.Model):
    TYPE_CHOICES = (
        ("text", "Text"),
        ("single", "Single Choice"),
        ("multiple", "Multiple Choice"),
    )

    question_id = models.AutoField(primary_key=True)
    question_content = models.TextField(verbose_name="question")
    is_active = models.BooleanField(default=True, verbose_name="activation")
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.question_content


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="question",
    )
    user = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="respondent",
    )
    text = models.CharField(max_length=255, verbose_name="answer")

    def __str__(self):
        return self.text
