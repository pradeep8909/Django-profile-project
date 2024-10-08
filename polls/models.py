import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
import csv
from django.http import HttpResponse

class Question(models.Model):
    ACTIVE = 0
    INACTIVE = 2
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    status = models.IntegerField (choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
