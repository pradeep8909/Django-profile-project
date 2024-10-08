from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ImageUploadForm
from .models import profile,user_role,role_type,Menus,RoleMainConfig,UserSchoolMapping
from django.shortcuts import render, redirect, get_object_or_404


def main_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Set session data
            request.session['user_image_url'] = user.userprofile.profile_picture.url
            user_role_obj = user_role.objects.get(user=user)
            request.session['role'] = user_role_obj.role.name

            if not user.is_superuser:
                try:
                    user_school_mapping = UserSchoolMapping.objects.get(user=user)
                    request.session['school_name'] = user_school_mapping.school.School_Name
                except UserSchoolMapping.DoesNotExist:
                    # If the user is not assigned any school, show a message and redirect to login page
                    return render(request, 'global/auth-signin.html', {
                        'error_message': "You are not assigned to any school. Please contact the principal or backend team."
                    })

            context = {
                'user_image_url': request.session.get('user_image_url'),
                'user_role': request.session.get('role'),
                'user_school': request.session.get('school_name'),
                'username': request.user.username,
            }
            return redirect('/dashboard', context)
        else:
            return HttpResponse("Invalid login details", status=401)
    return render(request, 'global/auth-signin.html')



"""""
def home(request):
    # Retrieve the session data
    user_image_url = request.session.get('user_image_url')
    user_role = request.session.get('role')
    user_school = request.session.get('school_name')
    print('User Image URL:', user_image_url)
    print('User Role:', user_role)
    print('User School:', user_school)


    context = {
        'user_image_url': user_image_url,
        'user_role': user_role,
        'user_school': user_school,
        'username': request.user.username,
    }
    return render(request, 'global/index.html', context)
"""
   

#upload the  imgae to the database !!!!!
#def update_profile(request):
 #   if request.method == 'POST':
  #      form = ImageUploadForm(request.POST, request.FILES, instance=request.user.profile)
   #     if form.is_valid():
    #        form.save()
     #       messages.success(request, 'Your profile was successfully updated!')
      #      return redirect('profile')
       # else:
       #     messages.error(request, 'Please correct the error below.')
    #else:
     #   form = ImageUploadForm(instance=request.user.profile)
    #return render(request, 'workprofile/profile.html', {'form': form})

##for viewing a image 

def image(request):
 
    return render(request, 'userprofile/index.html', {'profile': profile})


## user complete data 
from django.contrib.auth.models import User

def user_data(request):
    data=User.objects.values('username','email','first_name','last_name','id')
    data1=user_role.objects.all()
    return render(request, "global/user_data.html", {"data": data})



#user registeration
from .forms import UserCreationForm, UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            return redirect('/profile/user/')  
    else:
        form = UserCreationForm()
    return render(request, 'global/register.html', {'form': form})


## user data update or edit


def edit_profile(request,id):
    user = get_object_or_404(User, pk=id)
    
    # Ensure that only the user or an admin can edit the profile
    if request.user != user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this profile.')
        return redirect('/profile/user/')  
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/profile/user/', id=id)  
    else:
        form =UserUpdateForm(instance=user)
    return render(request, 'global/edit_profile.html', {'form': form, 'user': user})







