from django.db import models
from sineup.models import customuser

# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(customuser, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    status = models.CharField(max_length=30,default="In Progess")

    def __str__(self):
        return self.student.username