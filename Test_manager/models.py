from django.db import models
from django.template.defaultfilters import slugify
from User_manager.models import User, League
import datetime


# Create your models here.
class AllTest(models.Model):
    test_name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    for_league = models.ForeignKey('User_manager.League', on_delete=models.PROTECT)
    created_by = models.ForeignKey('User_manager.User', on_delete=models.PROTECT, null=True, blank=True)
    slug = models.CharField(max_length=200, unique=True, null=True, blank=True)
    questions = models.ManyToManyField("Questions", through="QuestionTest")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.test_name + " " + str(int(datetime.datetime.now().timestamp())))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.test_name


class QuestionTest(models.Model):
    test = models.ForeignKey("AllTest", on_delete=models.CASCADE, related_name="test")
    question = models.ForeignKey("Questions", on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.test.test_name


class Questions(models.Model):
    add_question = models.TextField(verbose_name="Treść pytania")
    question_possible_answer = models.ManyToManyField("Question_manager.AllPossibleAnswers", through="PossibleAnswers")
    question_correct_answer = models.ManyToManyField("Question_manager.AllPossibleAnswers", related_name="question_correct_answer", through="CorrectAnswer")
    for_league = models.ForeignKey("User_manager.League", on_delete=models.PROTECT)
    added_by = models.ForeignKey('User_manager.User', on_delete=models.PROTECT)
    added_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.add_question[:50] + " " + str(int(datetime.datetime.now().timestamp())))
        return super().save(*args, **kwargs)

class PossibleAnswers(models.Model):
    question = models.ForeignKey("Questions", on_delete=models.CASCADE)
    question_possible_answers = models.ForeignKey("Question_manager.AllPossibleAnswers", on_delete=models.CASCADE)

class CorrectAnswer(models.Model):
    question = models.ForeignKey("Questions", on_delete=models.CASCADE)
    question_correct_answers = models.ForeignKey("Question_manager.AllPossibleAnswers", on_delete=models.CASCADE)