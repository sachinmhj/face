from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class customuser(AbstractUser):
    Role = models.CharField(default=None,max_length=50)
    Imege = models.ImageField(upload_to="imaz",default=None)