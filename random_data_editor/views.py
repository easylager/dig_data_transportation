from django.shortcuts import render, HttpResponse
import os
from django.views.generic import View
from django import forms
from .utils import *


#абсолютные пути до основных директорый, используемых далее
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'files')
FULL_DATA_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'full_data.txt')
CLEAN_DATA_DIR = os.path.join(BASE_DIR, 'random_data_editor', 'clean_data.txt')

#форма для запроса строки
class CleanForm(forms.Form):
    string = forms.CharField(max_length=150)


def home_page(request):
    return render(request, 'random_data_editor/base.html')


def file_generator(path=FILES_DIR):
    n = 1
    for i in range(1, 10):
        print(f'{n}/101')
        n += 1
        with open(os.path.join(path, f'{i}.txt'), 'w') as file:
            for j in range(1, 100):
               string = random_string() + '\n'
               file.write(string)

file_generator()


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

    def post(self, request):
        bound_form = CleanForm(request.POST)
        if bound_form.is_valid():
            string = bound_form.cleaned_data['string']
            print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', string)
            lines_before, lines_after = clean_files(string=string)
            print(string)
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

