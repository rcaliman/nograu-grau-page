from django.shortcuts import render
from .forms import FormHoras
import datetime

def horas(request):
    hora_saida = None
    if request.POST:
        POST = request.POST
        input_entrada = [int(i) for i in POST.get('entrada').split(':')]
        entrada = datetime.timedelta(hours=input_entrada[0], minutes=input_entrada[1])
        input_almoco = [int(i) for i in POST.get('almoco').split(':')] or None
        almoco = datetime.timedelta(hours=input_almoco[0], minutes=input_almoco[1])
        input_volta_almoco = [int(i) for i in POST.get('volta_almoco').split(':')] or None
        volta_almoco = datetime.timedelta(hours=input_volta_almoco[0], minutes=input_volta_almoco[1])
        jornada = datetime.timedelta(hours=int(POST.get('jornada')), minutes=0)
        primeiro_periodo = almoco - entrada
        hora_saida = jornada - primeiro_periodo + volta_almoco
    return render(request, 'horas/calculo.html', {'form': FormHoras, 'hora_saida': hora_saida})
