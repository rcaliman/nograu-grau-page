from django.urls import path
from .views import mural

app_name = 'mural'

urlpatterns = [
    path('mural/', mural, name='mural'),
]
