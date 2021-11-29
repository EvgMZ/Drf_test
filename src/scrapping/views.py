from django.shortcuts import render
from .models import Vacancy


def home_page(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/index.html', context={'object_list': qs})

