from django.urls import path
from .views import bikefit_form, bikefit_result, previous_calcs, bikefit_links, bikefit_about

app_name = 'bikefit'

urlpatterns = [
    path('', bikefit_form, name='bikefit_form'),
    path('bikefit_result/', bikefit_result, name='bikefit_result'),
    path('previous_calcs/', previous_calcs, name='previous_calcs'),
    path('links/', bikefit_links, name='bikefit_links'),
    path('about/', bikefit_about, name='bikefit_about'),
]
