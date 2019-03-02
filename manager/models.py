from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    priority = models.SmallIntegerField() #0 low 1 medium 2 High
    status = models.SmallIntegerField() #0 new 1 accepted 2 completed 3cancel
    created_at = models.DateField(auto_now=True)