from .models.question import Question
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request) -> HttpResponse:
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
    }

    return render(request, "polls/index.html", context)

def detail(request, question_id:int) -> HttpResponse:
    question:Question = get_object_or_404(Question, id=question_id)

    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id:int) -> HttpResponse:
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)

def vote(request, question_id:int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")