from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg
from .models import T1


# Create your views here.


def douban(request):
    return HttpResponse('ok')


def book_sort(request):
    shorts = T1.objects.all()
    t = T1.objects.all()

    counter = t.count()
    if counter < 1:
        return HttpResponse('no')

    star_avg = f"{T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f}"
    sent_avg = \
        f"{T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f}"

    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    return render(request, 'result.html', locals())
