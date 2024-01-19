from django.urls import path
from apps.pcd.views import pcd_form, pcd_result, pcd_calculos_do_dia

app_name = 'pcd'

urlpatterns = [
    path('pcd/', pcd_form , name='pcd_form'),
    path('pcd_result/', pcd_result, name='pcd_result'),
    path('calculos_do_dia/', pcd_calculos_do_dia, name='pcd_calculos_do_dia')
]
