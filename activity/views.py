from django.shortcuts import render, get_object_or_404
from .models import Form, Section, Question, Option

def form_view(request, form_id, form_slug):
    # Get the specific form by ID and slug
    form = get_object_or_404(Form, id=form_id, slug=form_slug)
    print(form.name)

    
    # Get all sections related to this form
    sections = Section.objects.filter(form=form).order_by('order')
    for i in sections:
        print(i)
    
    # Get all questions related to these sections
    questions = Question.objects.filter(section_name__form=form).order_by('section_name','order')
    for j in questions:
        print(j.name,j.section_name,j.type,j.pk)
    # Get all options related to these questions
    options = Option.objects.filter(question_name__in=questions).order_by('order')
    
    context = {
        'form': form,
        'sections': sections,
        'questions': questions,
        'options': options,
    }
    print(context)

    return render(request, 'global/activity_main.html', context)

