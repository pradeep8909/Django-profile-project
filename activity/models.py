from django.db import models

from userprofile.models import BaseContent, Menus


class Form(BaseContent):
    PERIOD = ((0,'N/A'),(1,'DD'),(2,'MONTHLY'),(3,'Quarterly'),(4,'YEARLY'),(5,'ONE-TIME'))

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,unique=True)
    order = models.PositiveIntegerField()
    periodicity = models.PositiveIntegerField(choices=PERIOD , default=2)

    def __str__(self):
        return self.name

class Section(BaseContent):
    form = models.ForeignKey(Form , on_delete=models.CASCADE, related_name='form_name')
    name = models.CharField(max_length=200 )
    order = models.PositiveIntegerField()
    map = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Question(BaseContent):
    TYPE_CHOICE = (('T','Text Input'),('S','Select One Choice'),('MS','Multi Choice'),('R','Radiobutton'),('C','Checkbox'),('D','Date'),('F','File'))

    VALID_CHOICE = ((0,'Digit'),(1,'Number'),(2,'Alphabet'),(3,'Alphanumeric'))

    section_name = models.ForeignKey(Section , on_delete=models.CASCADE, related_name='section_name')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=2, choices=TYPE_CHOICE)
    order = models.PositiveIntegerField()
    mandatory = models.BooleanField(default=True)
    validation = models.IntegerField(choices=VALID_CHOICE)

    def __str__(self):
        return self.name
    


class Option(BaseContent):
    question_name = models.ForeignKey(Question , on_delete=models.CASCADE, related_name='question_name')
    text = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.text