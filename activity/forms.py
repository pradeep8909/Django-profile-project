from django import forms
from .models import Form, Section, Question, Option

class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name', 'slug', 'order', 'periodicity']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['form', 'name', 'order']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['section_name', 'name', 'type', 'order', 'mandatory', 'validation']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question_name', 'text', 'order']
