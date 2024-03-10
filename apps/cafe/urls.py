from django.urls import path
from .views import cafe_login, produtor_form, produtores, produtor, produtor_editar, produtor_apagar
from .views import cafe_form, cafes, cafe_editar, cafe, cafe_apagar
from .views import torra_form, torras, torra_editar, torra_apagar, torra, comparativo

app_name = 'cafe'

urlpatterns = [
    path('', cafe_login, name='cafe_login'),
    path('produtor_form/', produtor_form, name='produtor_form'),
    path('produtores/', produtores, name='produtores'),
    path('produtor/<int:produtor_id>', produtor, name='produtor'),
    path('produtor_editar/<int:produtor_id>', produtor_editar, name='produtor_editar'),
    path('produtor_apagar/<int:produtor_id>', produtor_apagar, name='produtor_apagar'),
    path('cafe_form/', cafe_form, name='cafe_form'),
    path('cafes/', cafes, name='cafes'),
    path('cafe_editar/<int:cafe_id>', cafe_editar, name='cafe_editar'),
    path('cafe_apagar/<int:cafe_id>', cafe_apagar, name='cafe_apagar'),
    path('cafe/<int:cafe_id>', cafe, name='cafe'),
    path('torra_form/', torra_form, name='torra_form'),
    path('torras/', torras, name='torras'),
    path('torra_editar/<int:torra_id>', torra_editar, name='torra_editar'),
    path('torra_apagar/<int:torra_id>', torra_apagar, name='torra_apagar'),
    path('torra/<int:torra_id>', torra, name='torra'),
    path('torra/comparativo', comparativo, name='comparativo'),
]
