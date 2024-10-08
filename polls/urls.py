from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path ("list/", views.question_list, name="question_list"),
    path ("edit/<int:question_id>/", views.edit_question, name="edit_question"),
    path("add/", views.add_question, name="add_question"),
    
    path("delete/<int:question_id>/", views.delete_question,name="delete_question"),
    
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # url for csv file upload
    path("uploadcsv/", views.upload_csv, name="upload_csv"),
    # download the csv file 
    path('download/questions/', views.download_questions_csv, name='download_questions_csv'),

    # making table for the global template
    path("table/", views.global_table, name="global_table"),

    # for changing the status of the question
    path('status/<int:question_id>/', views.question_status, name='question_status'),

    # for export the data using SQL
    path('export/questions/', views.export_questions, name='export_questions'),

    # for importing the data using Sql 
    path('import/', views.ImportQuestionsView.as_view(), name='import_questions'),

    #for getting the data with SQL query and set it in the table 
    path('table/sql/', views.sql_table, name='import_questions'),

    # for AjAX 
    path('get_questions/', views.get_questions, name='get_questions'),
    # print the question in the html page 
    path('listquestions/', views.show_questions, name='show_questions_page'),



    # url for API
    path('questions/', views.QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetail.as_view(), name='question-detail'),
    path('choices/', views.ChoiceList.as_view(), name='choice-list'),
    path('choices/<int:pk>/', views.ChoiceDetail.as_view(), name='choice-detail'),

]