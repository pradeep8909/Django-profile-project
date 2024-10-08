from beneficiary.models import BeneficiaryType , Beneficiary ,Grade
from django.shortcuts import render
from django.shortcuts import render, redirect ,get_object_or_404
from django.db.models import Count
from userprofile.models import UserSchoolMapping


def beneficiary_pie_chart(request):
    if request.user.is_superuser:
        # Admin sees all beneficiaries
        data = Beneficiary.objects.values('type__beneficiarytype').annotate(count=Count('id'))
    else:
        user_school_mapping = UserSchoolMapping.objects.get(user=request.user)
        school = user_school_mapping.school
        data = Beneficiary.objects.filter(location=school).values('type__beneficiarytype').annotate(count=Count('id'))

    print("pie chart ka data", data)
    
    labels = [entry['type__beneficiarytype'] for entry in data]
    values = [entry['count'] for entry in data]
    chart_data = zip(labels, values)  
    
    for entry in data:
        if entry['type__beneficiarytype'] == 'Student':
            request.session['student_count'] = entry['count']
        elif entry['type__beneficiarytype'] == 'Teacher':
            request.session['teacher_count'] = entry['count']

    context = {
        'chart_data': chart_data,  
    }
    return render(request, 'global/index.html', context)
