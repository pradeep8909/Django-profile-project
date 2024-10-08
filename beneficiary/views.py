from django.shortcuts import render
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from .forms import BeneficiaryForm
from .models import BeneficiaryType , Beneficiary ,Grade,School

## creating a beneficiary 


def create_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/beneficiary/table')
    else:
        form = BeneficiaryForm()
    return render(request, 'global/createbeneficiary.html', {'form': form})

## table data 
from userprofile.models import UserSchoolMapping

def beneficiary(request):
    if request.user.is_superuser:
        # Admin can see all beneficiaries
        data = Beneficiary.objects.all()
    else:
        user_school = UserSchoolMapping.objects.get(user=request.user).school
        school_id = user_school.id
        data = Beneficiary.objects.filter(location__id=school_id)

    return render(request, 'global/beneficiary.html', {'data': data})

"""""
def beneficiary(request):
    data= Beneficiary.objects.all()
    print(data)
    return render(request, 'global/beneficiary.html',{'data':data})

"""
## edit function

from django.shortcuts import render, get_object_or_404, redirect
from .models import Beneficiary

def edit_beneficiary(request, id):
    beneficiary = get_object_or_404(Beneficiary, id=id)

    if request.method == 'POST':
        beneficiary.beneficiaryname = request.POST['beneficiaryname']
        beneficiary.type_id = request.POST['type']  # Assuming this is the foreign key
        beneficiary.gradechoice_id = request.POST['gradechoice']  # Assuming this is the foreign key
        beneficiary.location_id = request.POST['location']  # Assuming this is the foreign key

        # Save the country, state, and district
        country_id = request.POST['country']
        state_id = request.POST['state']
        district_id = request.POST['district']
        
        # You should handle these if they are ForeignKeys or related fields
        # Add validation as necessary
        beneficiary.save()

        return redirect('/beneficiary/table')  # Redirect to your beneficiary table or another view

    return render(request, 'global/editbeneficiary.html', {
        'beneficiary': beneficiary,
        'beneficiary_types': BeneficiaryType.objects.all(),
        'grades': Grade.objects.all(),
        'schools': School.objects.all(),
        'countries': Location.objects.filter(location_level__name='Country'),
        'states': Location.objects.filter(location_level__name='State'),
        'districts': Location.objects.filter(location_level__name='District'),
    })




## views for the api 

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import BeneficiarySerializer

class BeneficiaryListCreateView(APIView):
    def get(self, request, format=None):
        beneficiaries = Beneficiary.objects.all()
        serializer = BeneficiarySerializer(beneficiaries, many=True)
        print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BeneficiarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeneficiaryRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Beneficiary.objects.get(pk=pk)
        except Beneficiary.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        beneficiary = self.get_object(pk)
        serializer = BeneficiarySerializer(beneficiary)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        beneficiary = self.get_object(pk)
        serializer = BeneficiarySerializer(beneficiary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        beneficiary = self.get_object(pk)
        serializer = BeneficiarySerializer(beneficiary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        beneficiary = self.get_object(pk)
        beneficiary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
##Demography ka kaam

from django.http import JsonResponse
from demography.models import Location 



def load_states(request):
    country_id = request.GET.get('country_id')
    states = Location.objects.filter(parent_id=country_id)
    return JsonResponse(list(states.values('id', 'name')), safe=False)

def load_districts(request):
    state_id = request.GET.get('state_id')
    districts = Location.objects.filter(parent_id=state_id)
    return JsonResponse(list(districts.values('id', 'name')), safe=False)

def load_schools(request):
    district_id = request.GET.get('district_id')
    schools = School.objects.filter(School_Locaion_id=district_id)
    return JsonResponse(list(schools.values('id', 'School_Name')), safe=False)



from django.contrib.auth.decorators import login_required

@login_required
def add_beneficiary(request):
    if request.method == 'POST':
        beneficiary_type_id = request.POST.get('type')
        beneficiary_name = request.POST.get('beneficiaryname')
        grade_id = request.POST.get('grade')
        school_id = request.POST.get('school')

        # Fetch the instances based on IDs
        beneficiary_type = BeneficiaryType.objects.get(id=beneficiary_type_id)
        grade = Grade.objects.get(id=grade_id)
        school = School.objects.get(id=school_id)
        
        # Create and save the new Beneficiary
        beneficiary = Beneficiary(
            type=beneficiary_type,
            beneficiaryname=beneficiary_name,
            gradechoice=grade,
            location=school
        )
        beneficiary.save()

        return redirect('/beneficiary/table/')  # Redirect after successful post

    else:
        # For GET request, display the form with options
        beneficiary_types = BeneficiaryType.objects.all()
        grades = Grade.objects.all()

        if request.user.is_superuser:
            # Admin can select any school
            countries = Location.objects.filter(location_level__name='Country')
            context = {
                'beneficiary_types': beneficiary_types,
                'grades': grades,
                'countries': countries,
                'is_admin': True,
            }
        else:
            # Non-admin users (teacher/principal) can add only to their own school
            user_school_mapping = UserSchoolMapping.objects.get(user=request.user)
            school = user_school_mapping.school
            district = school.School_Locaion
            state = district.parent
            country = state.parent

            context = {
                'beneficiary_types': beneficiary_types,
                'grades': grades,
                'selected_country': country,
                'selected_state': state,
                'selected_district': district,
                'selected_school': school,
                'is_admin': False,
            }

        return render(request, 'global/createbeneficiary.html', context)