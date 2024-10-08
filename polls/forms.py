
from django import forms
from .models import Question

class Question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','pub_date','status']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class uploadscsv_form(forms.Form):
    csv_file = forms.FileField()