import os
import sys
import django

from scrapping.pasr import *
from django.contrib.auth import get_user_model
import logging

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'drf_django_scrapping.settings'
django.setup()

from scrapping.models import City, Language, Vacancy, Url
from django.db import DatabaseError

User = get_user_model()
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)

pasrers = (
    (find_vac_hh, 'hh')
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id'])for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['Language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
urls = get_urls(settings)
#parsers = find_vac_hh(url)
#city = City.objects.filter(slug='moskva').first()
#language = Language.objects.filter(slug='python').first()
jobs = []
for data in urls:
    for job in pasrers:
        url = data['url_data']['hh']
        j = find_vac_hh(url, city=data['city'], language=data['language'])
        jobs += j

for job in jobs:
    try:
        v = Vacancy(**job)
        v.save()
    except DatabaseError:
        logging.error('Dont save in db')
