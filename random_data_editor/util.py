import os
import datetime
from datetime import datetime as dt
import random
import string
import sys
import re
import sqlite3

russian_alphabet = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'

def create_directory(path=os.path.curdir + '/' + 'files'):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def random_date_gen():
    start_date = datetime.date(2017, 1, 26)
    end_date = datetime.date(2022, 1, 26)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    res = dt.strftime(random_date, '%d.%m.%Y')
    #date = str(random_date).replace('-', '.')
    return res



def random_alpha_rus():
    res_str = ''
    for i in range(1, 11):
        res_str += str(random.choice(russian_alphabet))
    return res_str



def random_alpha_eng():
    res_str = ''
    for i in range(1, 11):
        res_str += str(random.choice(string.ascii_letters))
    return res_str




def random_numeric_full():
    res = random.randrange(1, 100000000)
    return res

def random_numeric_part():
    res = round(random.uniform(0, 20), 8)
    return res


def random_string():
    res = random_date_gen() + '//' + random_alpha_eng() + '//' + random_alpha_rus() + '//' + str(random_numeric_full()) + '//' + str(random_numeric_part()) + '//'
    return res



def join_files():
    ls = [i for i in os.listdir('./files') if i.endswith('.txt')]
    ls.sort()
    with open('full_data.txt', 'w') as f:
        for j in ls:
            s = open(f'./files/{j}').read()
            f.write(s)
            f.write('\n')
    return 'all files have been joined'




def count_lines(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        return len(lines)

def count_numbers(db):
    conn = sqlite3.connect(db)
    cu = conn.cursor()
    res = cu.execute('''select sum(number) from randomdata;''')
    #cu.execute('select sum(float)/(?) as mediana from randomdata;', number)
    return res

