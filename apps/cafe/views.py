import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ProdutorForm, CafeForm, TorraForm
from .models import ProdutorModel, CafeModel, TorraModel
import json


def cafe_login(request):
    if request.GET:
        fazer_logout = request.GET.get("logout")
        if fazer_logout:
            logout(request)
    if request.POST:
        POST = request.POST
        form = LoginForm(POST)
        if form.is_valid():
            autenticacao = authenticate(
                request,
                **{"username": POST.get("username"), "password": POST.get("password")}
            )
            if autenticacao:
                login(request, autenticacao)
    form = LoginForm
    form_action = reverse("cafe:cafe_login")
    return render(
        request, "cafe/pages/login.html", {"form": form, "form_action": form_action}
    )


@login_required(login_url="/cafe/")
def produtores(request):
    if request.POST:
        POST = request.POST
        if POST.get("produtor_id"):
            produtor = ProdutorModel.objects.get(id=POST["produtor_id"])
            form = ProdutorForm(POST, instance=produtor)
        else:
            form = ProdutorForm(POST)
        if form.is_valid():
            form.save()
    produtores = ProdutorModel.objects.all().order_by("-nome")
    return render(request, "cafe/pages/produtores.html", {"produtores": produtores})


@login_required(login_url="/cafe/")
def produtor(request, produtor_id):
    produtor = ProdutorModel.objects.get(id=produtor_id)
    return render(request, "cafe/pages/produtor.html", {"produtor": produtor})


@login_required(login_url="/cafe/")
def produtor_form(request):
    form = ProdutorForm
    form_action = reverse("cafe:produtores")
    return render(
        request,
        "cafe/pages/produtor_form.html",
        {"form": form, "form_action": form_action},
    )


@login_required(login_url="/cafe/")
def produtor_editar(request, produtor_id):
    produtor = ProdutorModel.objects.get(id=produtor_id)
    form_action = reverse("cafe:produtores")
    form = ProdutorForm(instance=produtor)
    return render(
        request,
        "cafe/pages/produtor_form.html",
        {
            "form": form,
            "form_action": form_action,
            "produtor_id": produtor_id,
        },
    )


@login_required(login_url="/cafe/")
def produtor_apagar(request, produtor_id):
    ProdutorModel.objects.get(id=produtor_id).delete()
    return redirect("cafe:produtores")


@login_required(login_url="/cafe/")
def cafe_form(request):
    form = CafeForm
    form_action = reverse("cafe:cafes")
    return render(
        request, "cafe/pages/cafe_form.html", {"form": form, "form_action": form_action}
    )


@login_required(login_url="/cafe/")
def cafes(request):
    if request.POST:
        POST = request.POST
        form = CafeForm(POST)
        if POST.get("cafe_id"):
            cafe = CafeModel.objects.get(id=POST["cafe_id"])
            form = CafeForm(POST, instance=cafe)
        if form.is_valid():
            form.save()
    cafes = CafeModel.objects.all().order_by("produtor__nome")
    return render(request, "cafe/pages/cafes.html", {"cafes": cafes})


@login_required(login_url="/cafe/")
def cafe_editar(request, cafe_id):
    cafe = CafeModel.objects.get(id=cafe_id)
    form = CafeForm(instance=cafe)
    form_action = reverse("cafe:cafes")
    return render(
        request,
        "cafe/pages/cafe_form.html",
        {
            "form": form,
            "cafe_id": cafe_id,
            "form_action": form_action,
        },
    )


@login_required(login_url="/cafe/")
def cafe(request, cafe_id):
    cafe = CafeModel.objects.get(id=cafe_id)
    return render(request, "cafe/pages/cafe.html", {"cafe": cafe})


@login_required(login_url="/cafe/")
def cafe_apagar(request, cafe_id):
    CafeModel.objects.get(id=cafe_id).delete()
    return redirect("cafe:cafes")


@login_required(login_url="/cafe/")
def torra_form(request):
    form = TorraForm
    form_action = reverse("cafe:torras")
    torra_id = ""
    if request.POST:
        lista_ids = request.POST.getlist("torra_id")
        if len(lista_ids) == 1:
            torra_id = lista_ids[0]
        if len(lista_ids) > 1:
            request.session["lista_ids"] = lista_ids
            return redirect("cafe:comparativo")
    if torra_id != "":
        torra = TorraModel.objects.get(id=torra_id)
        return render(
            request,
            "cafe/pages/torra_form.html",
            {"form": form, "form_action": form_action, "torra": torra},
        )
    return render(
        request,
        "cafe/pages/torra_form.html",
        {"form": form, "form_action": form_action},
    )


@login_required(login_url="/cafe/")
def torras(request):
    if request.POST:
        POST = request.POST
        dados_torra = {}
        for i in POST.keys():
            if i.isnumeric():
                dados_torra[i] = POST[i]
                POST._mutable = True
                POST["dados_torra"] = json.dumps(dados_torra)
                POST._mutable = False
        form = TorraForm(POST)
        if POST.get("torra_id"):
            torra = TorraModel.objects.get(id=POST["torra_id"])
            form = TorraForm(POST, instance=torra)
        if form.is_valid():
            form.save()
    torras = TorraModel.objects.all().order_by("-id")
    form_action = reverse("cafe:torra_form")
    return render(
        request,
        "cafe/pages/torras.html",
        {"torras": torras, "form_action": form_action},
    )


@login_required(login_url="/cafe/")
def torra_editar(request, torra_id):
    torra = TorraModel.objects.get(id=torra_id)
    form = TorraForm(instance=torra)
    form_action = reverse("cafe:torras")
    return render(
        request,
        "cafe/pages/torra_form.html",
        {"form": form, "form_action": form_action, "torra_id": torra_id},
    )


@login_required(login_url="/cafe/")
def torra_apagar(request, torra_id):
    TorraModel.objects.get(id=torra_id).delete()
    return redirect("cafe:torras")


@login_required(login_url="/cafe/")
def comparativo(request):
    lista_ids = request.session["lista_ids"]
    del request.session["lista_ids"]
    graphic = cria_grafico(lista_ids)
    return render(request, "cafe/pages/comparativo.html", {"graphic": graphic})


@login_required(login_url="/cafe/")
def torra(request, torra_id):
    torra = TorraModel.objects.get(id=torra_id)
    graphic = cria_grafico([torra_id])
    return render(
        request, "cafe/pages/torra.html", {"torra": torra, "graphic": graphic}
    )


def cria_grafico(torra_ids):
    plt.rcParams["figure.figsize"] = (13, 6.5)
    data = {}
    for id in torra_ids:
        torra = TorraModel.objects.get(id=id)
        dados_torra = dict([int(a), int(b)] for a, b in torra.dados_torra.items())
        data[id] = dados_torra
    df = pd.DataFrame(data)
    df.plot()
    buffer = io.BytesIO()
    plt.grid(True)
    plt.savefig(buffer, format="png")
    plt.figure().clear()
    buffer.seek(0)
    img_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(img_png)
    graphic = graphic.decode("utf-8")
    return graphic
