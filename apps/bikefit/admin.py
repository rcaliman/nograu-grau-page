from django.contrib import admin
from .models import ModelBikefit, ModelBikefitLinks, ModelBikefitAbout

@admin.register(ModelBikefit)
class AdminBikefit(admin.ModelAdmin):
    list_display = ['email', 'cavalo', 'esterno', 'braco', 'data']
    list_per_page = 25

@admin.register(ModelBikefitLinks)
class AdminBikefitLinks(admin.ModelAdmin):
    list_display = ['link', 'descricao']

@admin.register(ModelBikefitAbout)
class AdminBikefitAbout(admin.ModelAdmin):
    list_display = ['nome']