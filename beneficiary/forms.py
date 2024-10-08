"""""
from django import forms
from .models import Beneficiary, BeneficiaryType, Grade

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['beneficiaryname','type','gradechoice','location']
"""""

from django import forms
from .models import Beneficiary, BeneficiaryType, Grade, School
from demography.models import Location, LocationLevel

class BeneficiaryForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Location.objects.filter(location_level__name="Country"))
    state = forms.ModelChoiceField(queryset=Location.objects.none(), required=False)
    district = forms.ModelChoiceField(queryset=Location.objects.none(), required=False)
    
    class Meta:
        model = Beneficiary
        fields = ['country', 'state', 'district', 'beneficiaryname', 'type', 'gradechoice', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = Location.objects.filter(parent_id=country_id)
            except (ValueError, TypeError):
                pass
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = Location.objects.filter(parent_id=state_id)
            except (ValueError, TypeError):
                pass
