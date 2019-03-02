from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.SmallIntegerField() # 1 delivery person 2 store manager
