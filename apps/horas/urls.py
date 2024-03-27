from django.urls import path
from apps.horas.views import horas

app_name = 'horas'

urlpatterns = [
    path('horas/', horas, name='horas')
]
