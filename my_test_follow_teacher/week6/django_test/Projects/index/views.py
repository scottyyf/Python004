from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
# Create your views here.
from django.urls import reverse

from .models import Article, Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('id')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    return render(request, 'index/index.html', locals())


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'index/detail.html', locals())


def resutls(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'index/results.html', locals())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'index/detail.html', {
            'question': question,
            'error_message': 'you didnot select a choice'
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('index:results',
                                            args=(question.id,)))
    # return HttpResponse(f'you vote on question {question_id}')
