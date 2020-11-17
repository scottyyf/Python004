from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Name


# Create your views here.


def index(request, year):
    return HttpResponse(f'hello {year}')


def anydex(request):
    return redirect('/2020')


def x2020(request):
    return HttpResponse('you choose 2020')


def err(request, years):
    return render(request, 'yearview.html')


def books(request):
    n = Name.objects.all()
    return render(request, 'books.html', locals())
