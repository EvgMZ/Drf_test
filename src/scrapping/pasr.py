import requests
import codecs
from bs4 import BeautifulSoup as BS
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python'

__all__ = ('find_vac_hh',)

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept':
    'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'
}
jobs = []


def find_vac_hh(url, city=None, language=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_div = soup.find(
            'div',
            'vacancy-serp'
        )
        div_list = main_div.find_all(
            'div',
            attrs={'class': 'vacancy-serp-item'}
        )
        for div in div_list:
            title = div.find('a')
            name_vac = title.text
            href = title['href']
            company_name = div.find_all(
                'a',
                attrs={'class': 'bloko-link bloko-link_secondary'}
            )
            company_name = company_name[0].text
            try:
                description = div.find_all(
                    'div',
                    attrs={
                        'data-qa': 'vacancy-serp__vacancy_snippet_requirement'
                    }
                )
                description_two = div.find_all(
                    'div',
                    attrs={
                        'data-qa':
                        'vacancy-serp__vacancy_snippet_responsibility'
                    }
                )
                description = description_two[0].text + description[0].text
            except IndexError:
                description = 'Dont find desc'
            jobs.append(
                {
                    'title': name_vac,
                    'url': href,
                    'description': description,
                    'company': company_name,
                    'city_id': city,
                    'Language_id': language
                }
            )
    h = codecs.open('work.text', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
    return jobs
#find_vac_hh('https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python')