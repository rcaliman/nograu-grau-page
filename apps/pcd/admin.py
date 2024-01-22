from django.contrib import admin
from apps.pcd.models import ModelPCD

@admin.register(ModelPCD)
class AdminModelPCD(admin.ModelAdmin):
    list_display = ['codigo_banco', 'proxima_parcela', 'ultima_parcela', 'quantidade_parcelas','valor_parcela','valor_emprestado', 'data_calculo']
    list_per_page = 25
