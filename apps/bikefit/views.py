from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import FormBikefit, FormPreviousCalcs
from .utils.calculator import Calculator
from datetime import date
from .models import ModelBikefit, ModelBikefitLinks, ModelBikefitAbout
from django.contrib import messages
from django.http import Http404

HEAD_TEMPLATE = 'nograu/head.html'
NAVBAR_TEMPLATE = 'nograu/navbar.html'
TITLE_TEMPLATE = 'nograu/title.html'

def bikefit_form(request):
    data_bikefit_form = request.session.get('data_bikefit_form', None)
    form = FormBikefit(data_bikefit_form)
    form_action = reverse('bikefit:bikefit_result')
    labels = ('CAVALO', 'ESTERNO', 'BRAÇO', 'EMAIL')
    title = 'BIKE FIT VIRTUAL'
    subtitle = (
                'Digite com atenção suas medidas em CENTIMETROS e conforme as imagens.',
                'Exemplo: em uma medida de 1 metro e 65 centimetros digite 165.'
    )
    qty_bikefit_today = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()
    return render(request, 'nograu/bikefit/bikefit_form.html', 
                {
                    'form': form, 
                    'form_action': form_action, 
                    'labels': labels,
                    'title': title, 
                    'subtitle': subtitle,
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'qty_bikefit_today': qty_bikefit_today,
                })


def bikefit_result(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    form = FormBikefit(POST)
    request.session['data_bikefit_form'] = POST
    if form.is_valid():
        form.save()
        del(request.session['data_bikefit_form'])
        title = 'RESULTADOS'
        link = 'https://www.competitivecyclist.com/docs/competitivecyclist/fitcal/road-fit.pdf'
        subtitle = (
                'Este bike fit foi concebido de acordo com o metodo LeMond',
                f'e seguindo as especificacoes <a href={link} target=#>deste documento.</a>'
        )
        result = Calculator(**POST).result
        qty_bikefit_today = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()
        return render(request, 'nograu/bikefit/bikefit_result.html', 
                    {
                        'result': result,
                        'title': title,
                        'subtitle': subtitle,
                        'HEAD_TEMPLATE': HEAD_TEMPLATE,
                        'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                        'TITLE_TEMPLATE': TITLE_TEMPLATE,
                        'qty_bikefit_today': qty_bikefit_today,
                    })
    return redirect('bikefit:bikefit_form')

def previous_calcs(request):
    form_action = reverse('bikefit:previous_calcs')
    form = FormPreviousCalcs
    email = request.POST.get('email', None)
    previous_calcs = None
    qty_founded = None
    title = 'BUSCAR ANTERIORES'
    subtitle = ['Digite seu e-mail e clique em buscar para pesquisar calculos feitos anteriormente.',]
    if email:
        previous_data_calcs = ModelBikefit.objects.all().filter(email=email).order_by('-id')
        previous_calcs = [Calculator(**data).result() for data in previous_data_calcs.values()]
        qty_founded = previous_data_calcs.count()
        if not qty_founded > 0:
            messages.error(request, 'Não encontramos nenhum cálculo')

    qty_bikefit_today = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()
    return render(request, 'nograu/bikefit/previous_calcs.html',
                {
                    'form': form,
                    'form_action': form_action,
                    'previous_calcs': previous_calcs,
                    'qty_founded': qty_founded,
                    'title': title,
                    'subtitle': subtitle,
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'qty_bikefit_today': qty_bikefit_today,
                })

def bikefit_links(request):
    links = ModelBikefitLinks.objects.all().order_by('descricao')
    title = 'LINKS'
    subtitle = ['Os codigos deste site estao disponiveis no Github para uso livre.',
                'Qualquer duvida, critica ou sugestao podem ser enviadas pelo e-mail abaixo.']
    qty_bikefit_today = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()
    return render(request, 'nograu/bikefit/bikefit_links.html', 
                {
                    'title': title, 
                    'subtitle': subtitle,
                    'links': links,
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'qty_bikefit_today': qty_bikefit_today,
                })

def bikefit_about(request):
    title = 'SOBRE'
    subtitle = ['Os códigos desta pagina estao disponiveis no Github para uso livre.',]
    about = ModelBikefitAbout.objects.last() or None
    qty_bikefit_today = ModelBikefit.objects.all().filter(data=date.today().strftime('%Y-%m-%d')).count()
    return render(request, 'nograu/bikefit/bikefit_about.html', 
                {
                    'title': title,
                    'subtitle': subtitle,
                    'about': about,
                    'HEAD_TEMPLATE': HEAD_TEMPLATE,
                    'NAVBAR_TEMPLATE': NAVBAR_TEMPLATE,
                    'TITLE_TEMPLATE': TITLE_TEMPLATE,
                    'qty_bikefit_today': qty_bikefit_today,
                })