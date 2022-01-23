from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_page, name='home_page_url'),
    path('join/', Join_files.as_view(), name='join_files_url'),
    path('clean/', Join_files.as_view(), name='clean_files_url'),
    path('import/', import_db, name='import_files_url')
    ]