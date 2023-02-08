from django.db import models


class AllPossibleAnswers(models.Model):
    all_kind_answers = models.CharField(max_length=100)

    def __str__(self):
        return self.all_kind_answers
