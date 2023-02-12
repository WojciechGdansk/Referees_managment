from django.db import models
from User_manager.models import League, User
from Test_manager.models import QuestionTest


# Create your models here.
class OrganiseTest(models.Model):
    test_for_league = models.ForeignKey("League", on_delete=models.CASCADE)
    test_number = models.ForeignKey("QuestionTest", on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name="Data i godzina testu")


class UserSolving(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    test_number = models.ForeignKey("QuestionTest", on_delete=models.CASCADE)
    question = models.ForeignKey("QuestionTest", on_delete=models.CASCADE, related_name="question_from_test")
    user_response = models.CharField(max_length=100)
    result = models.FloatField()
