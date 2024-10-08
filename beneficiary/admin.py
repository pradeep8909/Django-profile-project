from django.contrib import admin
from django import forms
from .models import BeneficiaryType, Grade, Beneficiary,School

class BeneficiaryAdminForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['type', 'beneficiaryname', 'gradechoice','location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gradechoice'].queryset = Grade.objects.all()

class BeneficiaryAdmin(admin.ModelAdmin):
    form = BeneficiaryAdminForm
    list_display = ('beneficiaryname', 'type', 'gradechoice','location')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('School_Name', 'School_Code')
    search_fields = ('School_Name', 'School_Location','School_Code')
    list_filter = ('School_Name', 'School_Code')



admin.site.register(BeneficiaryType)
admin.site.register(Grade)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(School, SchoolAdmin)

