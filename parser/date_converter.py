# Def for convert string to date

import re
import time


def date_converter(string):
    """Return date from input string"""

    months_dict = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }

    raw_date = str(string[re.match('Обновлено', string).end()+2:]).replace(',', '')
    # Any number or letter before space: re.search '\w'
    day = int(raw_date[:re.search(r'\w+', raw_date).end()])
    # Word boundaries in line: re.search [а-я]
    month = months_dict[raw_date[re.search(r'[а-я]', raw_date).start():re.search(r'[а-я]+', raw_date).end()]]
    year = 2020
    str_date = f'{year}{month}{day}'
    date = time.strptime(str_date, '%Y%m%d')

    return time.strftime('%Y-%m-%d', date)
