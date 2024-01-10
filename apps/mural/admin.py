from django.contrib import admin
from .models import ModelMural

@admin.register(ModelMural)
class AdminModelMural(admin.ModelAdmin):
    actions_on_top = True
    list_display = ['nome', 'email', 'data', 'mensagem']