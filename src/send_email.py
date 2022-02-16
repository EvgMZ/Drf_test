import os
from socket import VMADDR_CID_ANY
import sys
from webbrowser import get
import django

from scrapping.pasr import *
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
import logging
import asyncio
import logging


logging.basicConfig(
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filename='main.log', filemode='a'
)
logger = logging.getLogger('__send_email__')
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'drf_django_scrapping.settings'
django.setup()


from scrapping.models import Vacancy
from drf_django_scrapping.settings import EMAIL_HOST_USER


empty = '<h2> No vac </h2>'
subject = 'Rass vac'
text_content = 'Rass vac'
from_email = EMAIL_HOST_USER
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
try:
    for i in qs:
        users_dct.setdefault((i['city'], i['language']), [])
        users_dct[(i['city'], i['language'])].append(i['email'])
    if users_dct:
        params = {'city_id__in': [], 'Language_id__in': []}
        for pair in users_dct.keys():
            params['city_id__in'].append(pair[0])
            params['Language_id__in'].append(pair[1])
        qs = Vacancy.objects.filter(**params).values()[:10]
        vacansies = {}
        for i in qs:
            vacansies.setdefault((i['city_id'], i['Language_id']), [])
            vacansies[(i['city_id'], i['Language_id'])].append(i)
        for keys, emails in users_dct.items():
            rows = vacansies.get(keys, [])
            html = ''
            for row in rows:
                html += f'<h5><a href="{ row["url"] }">{ row["title"] } </a></h5>'
                html += f'<p> {row["description"]}</p>'
                html += f'<p> {row["company"]}</p><br><hr>'
            _html = html if html else html
            for email in emails:
                to = email
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    from_email,
                    [to]
                )
                msg.attach_alternative(_html, 'text/html')
                msg.send()
except Exception as e:
    logger.error('Ошибка в отправке сообщения')
