from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.main_login, name="login"),
    
    ## user details 
    path("user/", views.user_data , name="user_data"),

    ## for the creation of the user 
    path('register/', views.register, name='register'),

    ## for the update or edit data of the user
    path('edit_profile/<int:id>/', views.edit_profile, name='edit_profile'),

]