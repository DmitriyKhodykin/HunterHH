# Module for Parsing features from resumes HH.ru

import requests
from bs4 import BeautifulSoup as Bs
from date_converter import date_converter as dc
import time
import re
# from requests.auth import HTTPBasicAuth
# from getpass import getpass


class Parser:
    """Parsing features from resumes HH.ru"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    def __init__(self, url):
        self.url = url

    def get_refs(self):
        """Returns refs to resume"""

        refs = []  # List of links to resume
        dates = []  # List of dates when resumes are updated

        for page in range(249):
            url = f'{self.url}&text=&page={page}'

            # main_page = requests.get(url, auth=HTTPBasicAuth('user', getpass()), headers=headers)
            main_page = requests.get(url, headers=self.headers)
            soup = Bs(main_page.content, 'html.parser')

            ref_containers = soup.find_all('div', class_='resume-search-item__header')
            dates_containers = soup.find_all('span', class_='resume-search-item__date')

            for ref in ref_containers:
                refs.append(f'https://hh.ru{ref.a.get("href")[:-30]}')

            for date in dates_containers:
                if 'новлено' in date.text:
                    dates.append(dc(date.text))

            time.sleep(1)

        return refs, dates

    def get_features(self, ref):
        """Return features from resume data"""

        resume_page = requests.get(ref, headers=self.headers)
        soup = Bs(resume_page.text, 'html.parser')

        try:
            title = soup.find('title').extract().text
        except (TypeError, ValueError, AttributeError):
            title = 'null'

        try:
            gender = soup.find('span', {'data-qa': 'resume-personal-gender'}).extract().text
        except (TypeError, ValueError, AttributeError):
            gender = 'null'

        try:
            city = soup.find('span', {'data-qa': 'resume-personal-address'}).extract().text
        except (TypeError, ValueError, AttributeError):
            city = 'null'

        try:
            age = int(soup.find('span', {'data-qa': 'resume-personal-age'}).extract().text[:2])
        except (TypeError, ValueError, AttributeError):
            age = 0

        try:
            salary = soup.find('span', {'data-qa': 'resume-block-salary'}).extract().text
            salary = int(salary[0:3])
        except (TypeError, ValueError, AttributeError):
            try:
                salary = soup.find('span', {'data-qa': 'resume-block-salary'}).extract().text
                salary = int(salary[0:2])
            except (TypeError, ValueError, AttributeError):
                salary = 0

        try:
            experience_s = soup.find('span', {
                'class': 'resume-block__title-text resume-block__title-text_sub'
                                            }).extract().text
            experience = str(experience_s)[12:re.search('лет', str(experience_s)).end()-4]
        except (TypeError, ValueError, AttributeError):
            experience = 'null'

        try:
            last_job = soup.find('div', {'class': 'resume-block__sub-title'}).extract().text
        except (TypeError, ValueError, AttributeError):
            last_job = 'null'

        return title, gender, city, age, salary, experience, last_job


if __name__ == "__main__":

    url = f'https://hh.ru/search/resume?L_is_autosearch=false&area={113}\
            &clusters=true&exp_period=all_time&logic=normal&no_magic=false&\
            order_by=relevance&pos=full_text&specialization={17.242}'

    parser = Parser(url)
    refs = parser.get_refs()[0]
    dates = parser.get_refs()[1]

    print(
        'Len list of refs:', len(refs),
        'Len list of dates:', len(dates)
    )
