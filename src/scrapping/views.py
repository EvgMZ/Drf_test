from django.shortcuts import render
from .models import Language, Vacancy
from .forms import FindForm


def home_page(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    print(language)
    print(city)
    qs = []
    _filter = {}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['Language__slug'] = language
    print(_filter)
    qs = Vacancy.objects.filter(**_filter)
    print(qs)
    return render(
        request,
        'scraping/index.html',
        context={'object_list': qs, 'form': form}
    )
