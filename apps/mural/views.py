from django.shortcuts import render
from django.urls import reverse
from .forms import FormModelMural
from .models import ModelMural
from django.contrib import messages
from .utils.pagination import make_pagination
from ..bikefit.models import ModelBikefit
from datetime import date

HEAD_TEMPLATE = 'nograu/head.html'
NAVBAR_TEMPLATE = 'nograu/navbar.html'
TITLE_TEMPLATE = 'nograu/title.html'
QTY_BIKEFIT_TODAY = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()


def mural(request):
    action_form = reverse('mural:mural')
    if request.POST:
        POST = request.POST
        request.session['mural_form_data'] = POST
        form = FormModelMural(POST)
        if form.is_valid():
            form.save()
            del(request.session['mural_form_data'])
            form = FormModelMural
            messages.success(request, 'Mensagem postada com sucesso!')
    else:
        form = FormModelMural
    posts = ModelMural.objects.all().order_by('-id')
    title = 'MURAL DE MENSAGENS'
    subtitle = ['Deixe suas mensagens, dúvidas e críticas construtivas. Por favor, tenham cortesia e educação.']
    page_obj, pagination_range = make_pagination(request, posts, 10)
    return render(request, 'nograu/mural/mural.html', {
        'form': form,
        'title': title,
        'subtitle': subtitle,
        'action_form': action_form,
        'posts': page_obj,
        'pagination_range': pagination_range,
        'HEAD_TEMPLATE': HEAD_TEMPLATE,
        'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
        'TITLE_TEMPLATE': TITLE_TEMPLATE,
        'qty_bikefit_today': QTY_BIKEFIT_TODAY,
    })
