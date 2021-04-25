from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    data = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'