from django.db import models
from django.contrib.auth.models import User
from manager.models import Task

class AcceptTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
