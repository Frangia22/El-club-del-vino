from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from Products.forms import registerForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

# Create your views here.
def index(request):
    return render(request, "products/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "registration/login.html", {"mensaje" : "El nombre de usuario o contraseña son incorrectos."})
    return render(request, "registration/login.html")


def register(request):

    if request.method == "GET":

        return render(

            request, "registration/register.html",

            {"form": registerForm}

        )

    elif request.method == "POST":

        form = registerForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

        return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return render(request, "products/index.html", {
        "mensaje": "Desconectado."
    })