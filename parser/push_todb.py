# Module for Pushing parsed data into a local database

from hh_parser import Parser
import MySQLdb  # pip install mysqlclient
import time
import auth


def pusher():
    """Push parsed data into a local db"""

    url = f'https://hh.ru/search/resume?L_is_autosearch=false&area={113}\
            &clusters=true&exp_period=all_time&logic=normal&no_magic=false&\
            order_by=relevance&pos=full_text&specialization={17.242}'

    db_smc = MySQLdb.connect(
        host=auth.host, user=auth.user,
        passwd=auth.passwd, db=auth.db, charset='utf8'
    )

    print('Get cursor() method for operations with local db')
    cursor = db_smc.cursor()
    prsr = Parser(url)
    refs = prsr.get_refs()[0]
    print(f'Len of refs list: {len(refs)}')
    dates = prsr.get_refs()[1]
    print(f'Len of dates list: {len(dates)}')

    print('Execute SQL-query')
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

        # The values to be added to the table
        values = (entrydate, title, gender, city, age, salary, experience, last_job, updated, link)

        # The SQL-query to the db table with reference to the variables
        if 30 < salary < 300:
            cursor.execute("""
                INSERT INTO 
                salesman_candidates (entrydate, title, gender, city, age, salary, experience, last_job, updated, link)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values)
            time.sleep(1)

    print('Commit')
    db_smc.commit()
    db_smc.close()


pusher()
