from django.shortcuts import render, redirect
from django.urls import reverse
from apps.pcd.forms import FormModelPCD, FormISPB
from apps.pcd.models import ModelPCD
from urllib.request import urlretrieve
from django.contrib import messages
from core.settings import BASE_DIR
import os
from datetime import datetime
from numpy_financial import rate, pv
import csv

HEAD_TEMPLATE = 'pcd/head.html'
NAVBAR_TEMPLATE = 'pcd/navbar.html'
TITLE_TEMPLATE = 'pcd/title.html'


def pcd_form(request):
    form_pcd = FormModelPCD(request.session.get('post_calcula_pcd', None))
    form_ispb = FormISPB(request.session.get('post_busca_ispb', None))
    
    data_bank_update = download_bank_info_file()

    today = datetime.now().strftime('%Y-%m-%d')
    quantidade_calculos = ModelPCD.objects.all().filter(data_calculo=today).count()

    return render(request, 'pcd/pcd_form.html', 
                {
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'action_form': reverse('pcd:pcd_result'),
                    'data_bank_update': data_bank_update,
                    'form_pcd': form_pcd,
                    'form_ispb': form_ispb,
                    'quantidade_calculos': quantidade_calculos,
                }
    )

def pcd_calculos_do_dia(request):
    today = datetime.now().strftime('%Y-%m-%d')
    dados = ModelPCD.objects.all().filter(data_calculo=today).order_by('-id')
    resultados = []
    for dado in dados:
        valor_emprestado = formata_valor(dado.valor_emprestado)
        valor_parcela = formata_valor(dado.valor_parcela)
        proxima_parcela = string_to_date(dado.proxima_parcela)
        ultima_parcela = string_to_date(dado.ultima_parcela)
        taxa_juros = calcula_taxa_de_juros(
                    dado.quantidade_parcelas,
                    valor_parcela,
                    valor_emprestado
                ),
        meses_em_ser = calcula_meses_em_ser(proxima_parcela, ultima_parcela)
        saldo_devedor = calcula_saldo_devedor(valor_parcela, taxa_juros[0], meses_em_ser)
        resultados.append(
            { 
                'banco': busca_banco(dado.codigo_banco),
                'proxima_parcela': proxima_parcela,
                'ultima_parcela': ultima_parcela,
                'quantidade_de_parcelas': dado.quantidade_parcelas,
                'valor_parcela': valor_parcela,
                'valor_emprestado': valor_emprestado,
                'data_calculo': dado.data_calculo,
                'taxa_de_juros': taxa_juros[0],
                'meses_em_ser': meses_em_ser,
                'saldo_devedor': saldo_devedor,
            }
        )

    today = datetime.now().strftime('%Y-%m-%d')
    quantidade_calculos = ModelPCD.objects.all().filter(data_calculo=today).count()
    return render(request, 'pcd/calculos_do_dia.html', 
        {
            'HEAD_TEMPLATE': HEAD_TEMPLATE,
            'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
            'TITLE_TEMPLATE': 'pcd/title_calculos_do_dia.html',
            'resultados': resultados,
            'title': 'CÁLCULOS DO DIA',
            'subtitle': ['Dados dos cálculos efetuados hoje',],
            'quantidade_calculos': quantidade_calculos,
        }
    )

def pcd_result(request):
    POST = request.POST
    if len(POST) <= 2:
        request.session['post_busca_ispb'] = POST
        form = FormISPB(POST)
        if form.is_valid():
            del(request.session['post_busca_ispb'])
            codigo_banco = POST['codigo_banco']
            resultado_ispb = {'banco': busca_banco(codigo_banco)}

            today = datetime.now().strftime('%Y-%m-%d')
            quantidade_calculos = ModelPCD.objects.all().filter(data_calculo=today).count()

            return render(request, 'pcd/pcd_result.html',
                {
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'resultado_ispb': resultado_ispb,
                    'quantidade_calculos': quantidade_calculos,
                })
        else:
            return redirect('pcd:pcd_form')
    else:
        form = FormModelPCD(POST)
        request.session['post_calcula_pcd'] = POST
        if form.is_valid():
            form.save()
            resultado_pcd = calcula_pcd(POST)
            if resultado_pcd['quantidade_de_parcelas'] < 1 or \
                    resultado_pcd['valor_parcela'] < 1 or \
                    resultado_pcd['valor_emprestado'] < 1 or \
                    resultado_pcd['taxa_de_juros'] < 1:
                messages.error(request, '''Existe algum erro nesses dados,
                               lembre-se que todos os algarismos devem ser digitados,
                               inclusive zeros à direita, sem vírgulas, pontos ou espaços''')
                return redirect('pcd:pcd_form')
            del(request.session['post_calcula_pcd'])
            today = datetime.now().strftime('%Y-%m-%d')
            quantidade_calculos = ModelPCD.objects.all().filter(data_calculo=today).count()

            return render(request, 'pcd/pcd_result.html',
                {
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'resultado_pcd': resultado_pcd,
                    'quantidade_calculos': quantidade_calculos,
                })  
        else:
            return redirect('pcd:pcd_form')

def calcula_pcd(POST):
    codigo_banco = POST['codigo_banco']
    data_proxima_parcela = string_to_date(POST['proxima_parcela'])
    data_ultima_parcela = string_to_date(POST['ultima_parcela'])
    quantidade_de_parcelas = int(POST['quantidade_parcelas'])
    valor_parcela = formata_valor(POST['valor_parcela'])
    valor_emprestado = formata_valor(POST['valor_emprestado'])
    taxa_juros = calcula_taxa_de_juros(
        POST['quantidade_parcelas'],
        POST['valor_parcela'],
        POST['valor_emprestado']
    )
    meses_em_ser = calcula_meses_em_ser(data_proxima_parcela, data_ultima_parcela)
    saldo_devedor = calcula_saldo_devedor(valor_parcela, taxa_juros, meses_em_ser)

    resultado_pcd = {
                'banco': busca_banco(codigo_banco),
                'data_proxima_parcela': data_proxima_parcela,
                'data_ultima_parcela': data_ultima_parcela,
                'quantidade_de_parcelas': quantidade_de_parcelas,
                'valor_parcela': valor_parcela,
                'valor_emprestado': valor_emprestado,
                'taxa_de_juros': taxa_juros,
                'meses_em_ser': meses_em_ser,
                'saldo_devedor': saldo_devedor,
            }
    
    return resultado_pcd

def calcula_saldo_devedor(valor_parcela, taxa_de_juros, meses_em_ser):
    saldo_devedor = abs(pv(taxa_de_juros/100, int(meses_em_ser), valor_parcela))
    return saldo_devedor
        
def download_bank_info_file():
    url_lista_bancos = 'https://www.bcb.gov.br/content/estabilidadefinanceira/str1/ParticipantesSTR.csv'
    destino = BASE_DIR / 'apps' / 'pcd' / 'lista_de_bancos.csv'
    if not os.path.isfile(destino):
        urlretrieve(url_lista_bancos, destino)
    stat_file = os.stat(destino)
    data_arquivo = datetime.fromtimestamp(stat_file.st_mtime).strftime('%d/%m/%Y')
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    if data_arquivo != data_hoje:
        urlretrieve(url_lista_bancos, destino)
    return data_arquivo

def string_to_date(string_data: str):
    dia, mes, ano = string_data[0:2], string_data[2:4], string_data[4:]
    return datetime(int(ano), int(mes), int(dia))

def calcula_taxa_de_juros(quantidade_parcelas, valor_parcela, valor_emprestado) -> float:
    quantidade_parcelas = int(quantidade_parcelas)
    valor_parcela = float(valor_parcela)
    valor_emprestado = float(valor_emprestado)
    taxa_de_juros = rate(
        quantidade_parcelas, 
        -valor_parcela, 
        valor_emprestado, 0
    ) * 100
    return taxa_de_juros

def calcula_meses_em_ser(data_proxima_parcela, data_ultima_parcela):
    anos_faltantes = data_ultima_parcela.year - data_proxima_parcela.year
    meses_faltantes = data_ultima_parcela.month - data_proxima_parcela.month
    return (anos_faltantes) * 12 + 1 + meses_faltantes

def formata_valor(valor_parcela:str) -> float:
    inteiros = valor_parcela[:-2]
    centavos = valor_parcela[-2:]
    return float(inteiros + '.' + centavos)

def busca_banco(codigo_banco):
    arquivo = BASE_DIR / 'apps' / 'pcd' / 'lista_de_bancos.csv'
    with open(arquivo, encoding='utf-8') as f:
        reader = csv.reader(f)
        for linha in reader:
            ispb, nome_reduzido, numero_codigo, \
            participa_da_compe, acesso_principal, \
            nome_extenso, inicio_da_operacao = linha
            if codigo_banco == numero_codigo:
                return {
                    'numero_codigo': numero_codigo,
                    'numero_ispb': ispb,
                    'nome_extenso': nome_extenso
                }
        return {
                'numero_codigo': codigo_banco,
                'numero_ispb': 'não encontrado',
                'nome_extenso': 'código provavelmente inválido',
        }
            
