from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_page, name='home_page_url'),
    path('join', join_files, name='join_files_url'),
    ]