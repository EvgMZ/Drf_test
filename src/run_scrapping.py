import os
import sys
import django
from datetime import datetime as dt
from scrapping.pasr import *
from django.contrib.auth import get_user_model
import logging
import asyncio
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
jobs = []


async def main(value):
    func, url, city, language = value
    job = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id'])for q in qs)
    print(settings_list)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    print(qs)
    url_dct = {(q['city_id'], q['Language_id']): q['url_data'] for q in qs}
    print(url_dct)
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

loop = asyncio.get_event_loop()
tmp_tasks = [
    (find_vac_hh, data['url_data']['hh'], data['city'], data['language'])
    for data in urls
    for job in pasrers
]
tasks = asyncio.wait([loop.create_task(main(f))for f in tmp_tasks])

#for data in urls:
#    for job in pasrers:
#        url = data['url_data']['hh']
#        j = find_vac_hh(url, city=data['city'], language=data['language'])
#        jobs += j
loop.run_until_complete(tasks)
loop.close()
for job in jobs:
    try:
        v = Vacancy(**job)
        v.save()
    except DatabaseError:
        logging.error('Dont save in db')


ten_day_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_day_ago).delete()