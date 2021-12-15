from django.shortcuts import render
from .models import Language, Vacancy
from .forms import FindForm
from django.core.paginator import Paginator

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
    _filter = {}
    context = {'city': city, 'Language': language, 'form': form}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['Language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(
        request,
        'scraping/list.html',
        context=context
    )
