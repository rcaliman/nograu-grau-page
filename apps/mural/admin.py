from django.contrib import admin
from .models import ModelMural

@admin.register(ModelMural)
class AdminModelMural(admin.ModelAdmin):
    ...