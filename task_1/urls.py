
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('random_data_editor.urls')),
    path('admin/', admin.site.urls),

]
