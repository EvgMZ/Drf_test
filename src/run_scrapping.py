import os
import sys

import django

from scrapping.pasr import find_vac_hh


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'drf_django_scrapping.settings'
django.setup()

from scrapping.models import City, Language, Vacancy
from django.db import DatabaseError


parsers = find_vac_hh()
city = City.objects.filter(slug='moskva').first()
language = Language.objects.filter(slug='Python').first()

for job in parsers:
    v = Vacancy(**job, city=city, Language=language)
    try:
        v.save()
    except DatabaseError:
        pass
