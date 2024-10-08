from django.urls import path
from . import views

urlpatterns = [
    path('<int:form_id>/<slug:form_slug>/', views.form_view, name='create_form'),
]