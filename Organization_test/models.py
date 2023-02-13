from django.db import models
from User_manager.models import League, User
from Test_manager.models import QuestionTest
import datetime
from django.template.defaultfilters import slugify

# Create your models here.
class OrganiseTest(models.Model):
    test_for_league = models.ForeignKey("User_manager.League", on_delete=models.CASCADE)
    test_number = models.ForeignKey("Test_manager.AllTest", on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name="Data i godzina testu")
    slug = models.CharField(max_length=200, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.date_time) + str(self.test_for_league) + " " +
                                str(int(datetime.datetime.now().timestamp())))
        return super().save(*args, **kwargs)


class UserSolving(models.Model):
    user = models.ForeignKey("User_manager.User", on_delete=models.CASCADE)
    test_number = models.ForeignKey("Test_manager.AllTest", on_delete=models.CASCADE)
    question = models.ForeignKey("Test_manager.QuestionTest", on_delete=models.CASCADE, related_name="question_from_test")
    user_response = models.CharField(max_length=100)
    result = models.FloatField()

