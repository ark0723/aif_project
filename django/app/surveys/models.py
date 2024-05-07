from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, related_name="questions", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    TYPE_CHOICES = (
        ("text", "Text"),
        ("single", "Single Choice"),
        ("multiple", "Multiple Choice"),
    )
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    text = models.TextField()

    def __str__(self):
        return self.text
