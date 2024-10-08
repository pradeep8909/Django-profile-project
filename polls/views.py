from django.db.models import F
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from .models import Choice, Question

#from .forms import Question_form
#from django.db.models import Max

import csv
from .forms import uploadscsv_form
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def question_list(request):
    questions = Question.objects.all()
    #q = Question.pub_date
    #date=Question.pub_date()
        
    
    return render(request, "polls/table.html", {"questions": questions})
    #return HttpResponse(Question_list)


def edit_question(request, question_id):
    item = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        item.question_text = request.POST.get('question_text')
        item.pub_date = request.POST.get('pub_date')
        item.save()
        return redirect('/polls/table/') 

    return render(request, 'polls/edit.html', {'item': item})
    

def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        pub_date = request.POST.get('pub_date')
        if question_text and pub_date:
            try:
                # Convert the pub_date to a datetime object
                pub_date = timezone.datetime.strptime(pub_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                return render(request, 'polls/add_question.html', {'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM.'})

            # Create and save the new question
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()

        return redirect('/polls/table/')  # Redirect to a page showing the list of questions

    return render(request, 'polls/add_question.html')




def delete_question(request, question_id):
    item = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        item.delete()
        return redirect('/polls/table/')  # Change 'some_view_name' to the name of the view you want to redirect to
    else:
        return render(request, 'polls/delete.html',{'item':item})

# view for uploading question from csv file 

def upload_csv(request):
    if request.method == 'POST':
        form = uploadscsv_form(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                question_text = row.get('question_text')
                pub_date = timezone.now()



                # Save each row as a Question object
                Question.objects.create(question_text=question_text, pub_date=pub_date)

            messages.success(request, 'CSV file uploaded and data saved successfully!')
            return redirect('/polls/table/')
    else:
        form = uploadscsv_form()
    
    return render(request, 'polls/uploadcsv.html', {'form': form})


# for download the csv file 

def download_questions_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questions.csv"'

    writer = csv.writer(response)
    writer.writerow([ 'question_text', 'pub_date'])

    questions = Question.objects.all().values_list( 'question_text', 'pub_date')
    for question in questions:
        writer.writerow(question)

    return response

## Global table
from django.core.paginator import Paginator

def global_table(request):
    data = Question.objects.all().order_by('id')

    ##getting data in the pages format 
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'global/tbl_bootstrap.html', {'page_obj': page_obj})

from django.contrib.auth.decorators import login_required

@login_required
def question_status(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.status == 0:
        question.status = 2
    else:
        question.status = 0
    question.save()
    return redirect('/polls/table/') 

## exporting the data using SQL query 
from django.db import connection


def export_questions(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export_questions.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Question Text', 'Publication Date'])

    # raw SQL query to fetch questions
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, question_text, pub_date FROM polls_question")
        rows = cursor.fetchall()

        for row in rows:
            writer.writerow(row)

    return response


## importing the data into the database using SQl query
from django.core.files.storage import FileSystemStorage

class ImportQuestionsView(View):
    def get(self, request):
        return render(request, 'global/import_questions.html')

    def post(self, request):
        if 'csv_file' not in request.FILES:
            return HttpResponse("No file uploaded")

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return HttpResponse("File is not a CSV")

        # Save the file to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header row

            if header is None or header != ['question_text']:
                return HttpResponse("CSV file has incorrect header format")

            with connection.cursor() as cursor:
                for row_index, row in enumerate(reader, start=1):
                    if len(row) == 1:
                        question_text = row[0]

                        pub_date = timezone.now()
                        status = 0

                        try:
                            cursor.execute(
                                """
                                INSERT INTO polls_question (question_text, pub_date, status)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (id) DO UPDATE SET question_text = EXCLUDED.question_text
                                """,
                                [question_text, pub_date, status]
                            )
                        except Exception as e:
                            return HttpResponse(f"Error inserting row {row_index}: {e}")
                    else:
                        return HttpResponse(f"CSV file has incorrect format on row {row_index}")

        return  redirect('/polls/table/') 



#### geting the data and print it into table using SQL query 

def sql_table(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, question_text, pub_date, status
            FROM polls_question
            ORDER BY id
        """)
        rows = cursor.fetchall()
    # Prepare context with the data

    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'global/polls_sql_listing.html', context)



## getting the data from databse usig AJAX
from django.http import JsonResponse

def get_questions(request):
    questions = Question.objects.all().values('id', 'question_text', 'pub_date', 'status').order_by('id')
    questions_list = list(questions)
    return JsonResponse(questions_list, safe=False)
# show the data in the html 
def show_questions(request):
    return render(request, 'global/questions_list.html')


#views of API
from rest_framework import generics
from .serializers import QuestionSerializer, ChoiceSerializer

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer