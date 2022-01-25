from django.shortcuts import render, HttpResponse
import os
from django.views.generic import View
from django import forms
import sqlite3
import sys
import re
from .utils import *


#абсолютные пути до основных директорый, используемых далее
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'files')
FULL_DATA_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'full_data.txt')
CLEAN_DATA_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'clean_data.txt')
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

#форма для запроса строки
class CleanForm(forms.Form):
    string = forms.CharField(max_length=150)


def home_page(request):
    return render(request, 'random_data_editor/base.html')

#функция генерирует 100 файлов с заданым содержанием(каждая строчка - это результат работы функции random_string
#функция random_string - это результат работы 5 функций, генерирующих случайный набор символов, каждая функция имеет свою облость данных
def file_generator(path=FILES_DIR):
    n = 1
    for i in range(1, 10):
        print(f'{n}/101')
        n += 1
        with open(os.path.join(path, f'{i}.txt'), 'w') as file:
            for j in range(1, 100):
               string = random_string() + '\n'
               file.write(string)

#file_generator()

#класс наследуется от встроенного в фреймворк метакласса View, метод get иполняет обьединение
#всех файлов из директории files/ в один и возвращает форму, для ввода пользователем строки, строки содержащие которую будут удалены
class Join_files(View):
    def get(self, request):
        files_list = [i for i in os.listdir(FILES_DIR) if i.endswith('.txt')]
        files_list.sort()
        with open('full_data.txt', 'w') as join_file:
            for j in files_list:
                s = open(f'{FILES_DIR}/{j}').read()
                join_file.write(s)
                join_file.write('\n')
        form = CleanForm()
        return render(request, 'random_data_editor/join.html', context={'form': form})

#метод post очищает форму, валидирует, подсчитывет количество строк в файле до очисти и после и фозвращает полученный значения в html шаблон
    def post(self, request):
        bound_form = CleanForm(request.POST)
        if bound_form.is_valid():
            string = bound_form.cleaned_data['string']
            lines_before, lines_after = clean_files(string=string)
            return render(request, 'random_data_editor/after_clean.html', context={'lines_before': lines_before, 'lines_after': lines_after})
        return render(request, 'random_data_editor/join.html', context={'form': bound_form})


def clean_files(string: str, input=FULL_DATA_DIR, output=CLEAN_DATA_DIR):
    lines_before = f'before clean: {count_lines(input)}'
    if input:
        with open(input, 'r+') as ipt:
            with open(output, 'w') as otp:
                lines = ipt.readlines()
                for line in lines:
                    if string not in line:
                        otp.write(f'{line}')
    lines_after = f'after clean: {count_lines(output)}'
    return lines_before, lines_after


def count_lines(path):
    res = sum(1 for line in open(path, 'r'))
    return res


#Создается таблица в базе данных, если запрос выполняется впервые,
# иначе таблица очищается и  в нее импортируется все данные из файла 'full_data.txt'
def import_db(request, db=DB_PATH):
    conn = sqlite3.connect(db)
    cu = conn.cursor()
    cu.execute('''create table if not exists randomdata
    (date VARCHAR(255), eng VARCHAR(255), rus VARCHAR(255), number VARCHAR(255), float VARCHAR(255))''')
    cu.execute('delete from randomdata')
    with open(FULL_DATA_DIR, 'r+') as f1:
        n = 1
        lines = f1.readlines()
        lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
        m = len(lines)
        for line in lines:
            content_list = re.split('//', line)[:-1]

            cu.execute('insert into randomdata(date, eng, rus, number, float) values(?,?,?,?,?);', content_list)
            n += 1
        conn.commit()
        conn.close()
        return render(request, 'random_data_editor/import_to_db.html', context={'n': n - 1, 'm': m})


#в функции устанавливается связь с базой данный, в которой находится таблица, где собрана вся информация из 100 файлов
def sum_and_median(request, db=DB_PATH):
    conn = sqlite3.connect(db)
    cu = conn.cursor()
    #запрос на получение суммы всех целых чисел
    cu.execute('select sum(number) from randomdata')
    sum = cu.fetchone()[0]
    #запрос на получение медианы всех дробных чисел
    cu.execute('select float from (select float from randomdata order by float desc limit (select count(*) from randomdata)/2) as mediana_table order by float desc limit 1;')
    median = cu.fetchone()[0]
    #функция возвращает сумму и медиану в html шаблон
    return render(request, 'random_data_editor/sum_and_median.html', context={'sum': sum, 'median': median})
#import_db()
#print(sum_numbers(db=DB_PATH))