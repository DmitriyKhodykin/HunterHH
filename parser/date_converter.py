# Def for convert string to date

import re
import time


def date_converter(string):
    """Return date from input string"""

    months_dict = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }

    raw_date = string[re.match('Обновлено', string).end()+2:]
    day = int(raw_date[:re.search(' ', raw_date).end()-1])
    month = months_dict[raw_date[re.search(' ', raw_date).end():re.search(',', raw_date).end()-1]]
    year = 2020
    str_date = f'{year}{month}{day}'
    date = time.strptime(str_date, '%Y%m%d')

    return time.strftime('%Y-%m-%d', date)
