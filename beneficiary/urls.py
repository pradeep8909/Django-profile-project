from django.urls import path

from . import views

from .views import BeneficiaryListCreateView, BeneficiaryRetrieveUpdateDestroyView

urlpatterns = [
    # Beneficiary Table 
    path('table/', views.beneficiary, name='beneficiary'),


    # Creatinga a new Beneficiary
   # path('createbeneficiary/', views.create_beneficiary, name='create_beneficiary'),
    path('createbeneficiary/', views.add_beneficiary, name='createbeneficiary'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-schools/', views.load_schools, name='ajax_load_schools'),



    # to edit the beneficiary 
    path('edit/<int:id>/', views.edit_beneficiary, name='edit_beneficiary'),

    #api urs 
    path('beneficiaries/', BeneficiaryListCreateView.as_view(), name='beneficiary-list-create'),
    
    path('beneficiaries/<int:pk>/', BeneficiaryRetrieveUpdateDestroyView.as_view(), name='beneficiary-detail'),

    # pie chart
    #path('beneficiarychart/', views.beneficiary_pie_chart, name='beneficiarychart'),

]