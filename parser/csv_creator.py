# Module for Pushing parsed data into a csv file

from hh_parser import Parser
import time
import pandas as pd


def csv_creator():
    """Push parsed data into a csv"""

    url = f'https://hh.ru/search/resume?L_is_autosearch=false&area={113}\
            &clusters=true&exp_period=all_time&logic=normal&no_magic=false&\
            order_by=relevance&pos=full_text&specialization={17.242}'

    prsr = Parser(url)
    refs = prsr.get_refs()[0]
    print(f'Len of refs list: {len(refs)}')
    dates = prsr.get_refs()[1]
    print(f'Len of dates list: {len(dates)}')

    data = pd.DataFrame(
        columns=['entrydate', 'title', 'gender', 'city', 'age', 'salary', 'experience', 'last_job', 'updated', 'link']
    )

    print('Execute query')
    for ref, dat in zip(refs, dates):
        # Def variables and their values
        entrydate = time.strftime("%Y-%m-%d")
        title = prsr.get_features(ref)[0]
        gender = prsr.get_features(ref)[1]
        city = prsr.get_features(ref)[2]
        age = prsr.get_features(ref)[3]
        salary = prsr.get_features(ref)[4]
        experience = prsr.get_features(ref)[5]
        last_job = prsr.get_features(ref)[6]
        updated = dat
        link = ref

        if 30 < salary < 300:
            data = data.append({
                'entrydate': entrydate,
                'title': title,
                'gender': gender,
                'city': city,
                'age': age,
                'salary': salary,
                'experience': experience,
                'last_job': last_job,
                'updated': updated,
                'link': link
            }, ignore_index=True)

    return data


csv_creator().to_csv('csv_data.csv')
