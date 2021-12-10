from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reg(request):
    if request.method == "POST":
        username = request.POST.get('login', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        passwordConfirm = request.POST.get('passwordConfirm', None)
        if password != passwordConfirm:
            error = "Пароли не совпадают"
            return render(request, 'reg.html', locals())
        users = User.objects.all()
        for i in users:
            if i.username == username:
                error = "Пользователь с таким логином уже существует"
                return render(request, 'reg.html', locals())
            if i.email == email:
                error = "Пользователь с такой почтой уже существует"
                return render(request, 'reg.html', locals())
        user = User.objects.create_user(username=username, password=password, email=email)
        return render(request, 'reg.html', locals())
    return render(request, 'reg.html', locals())

@csrf_exempt
def login_(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    username = request.POST.get('login', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error = "Учетная запись не активирована"
            return render(request, 'index.html', locals())
    else:
        error = "Неверный логин или пароль"
        return render(request, 'index.html', locals())

@csrf_exempt
def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')
