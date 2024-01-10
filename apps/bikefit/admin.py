from django.contrib import admin
from .models import ModelBikefit, ModelBikefitLinks, ModelBikefitAbout

@admin.register(ModelBikefit)
class AdminBikefit(admin.ModelAdmin):
    ...

@admin.register(ModelBikefitLinks)
class AdminBikefitLinks(admin.ModelAdmin):
    ...

@admin.register(ModelBikefitAbout)
class AdminBikefitAbout(admin.ModelAdmin):
    ...