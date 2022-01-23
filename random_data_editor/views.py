from django.shortcuts import render
import os
from django import forms
from utils import *


#абсолютные пути до основных директорый, используемых далее
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'files')
FULL_DATA_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'full_data.txt')


#форма для запроса строки
class CleanForm(forms.Form):
    string = forms.CharField(max_length=150)


def home_page(request):
    return render(request, 'random_data_editor/base.html')


def file_generator(request, path):
    n = 1
    for i in range(1, 101):
        print(f'{n}/101')
        n += 1
        with open(os.path.join(path, f'{i}.txt'), 'w') as file:
            for j in range(1, 100000):
               string = random_string() + '\n'
               file.write(string)

def join_files():
    files_list = [i for i in os.listdir(FILES_DIR) if i.endswith('.txt')]
    files_list.sort()
    with open('full_data.txt', 'w') as join_file:
        for j in files_list:
            s = open(f'{FILES_DIR}/{j}').read()
            join_file.write(s)
            join_file.write('\n')
    #form = CleanForm()
    #return render(request, 'random_data_editor/join.html', context={'form': form})


def clean_files(slug: str, input=FULL_DATA_DIR):
    print(f'before clean: {count_lines(input)}')
    if input:
        with open(input, 'r+') as input:
            lines = input.readlines()
            for line in lines:
                if slug not in line:
                    input.write(f'{line}')
    print(f'after clean: {count_lines(input)}')
    #return render(request, '')

join_files()
clean_files('ff')