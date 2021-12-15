from django.shortcuts import render
from .models import Language, Vacancy
from .forms import FindForm


def home_page(request):
    form = FindForm()
    return render(
        request,
        'scraping/index.html',
        context={'form': form}
    )


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    _filter = {}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['Language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(
        request,
        'scraping/list.html',
        context={'object_list': qs, 'form': form}
    )
