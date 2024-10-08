from django import forms
from .models import profile
from .models import user_role ,role_type
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['user', 'profile_picture']

## for the creation of the user

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ModelChoiceField(queryset=role_type.objects.all(), required=True)


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','role','last_name','password1', 'password2')   

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_role.objects.create(user=user, role=self.cleaned_data['role'])
        return user      

##for updating the data of the user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ModelChoiceField(queryset=role_type.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','role')       


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_role_obj, created = user_role.objects.get_or_create(user=user)
            user_role_obj.role = self.cleaned_data['role']
            user_role_obj.save()
            
        return user    
