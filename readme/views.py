from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from readme.forms import RegisterForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import datetime


@login_required(login_url='/landing-page', redirect_field_name=None)
def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'readme/index.html', context=context)


def landing(request):
    return render(request, 'readme/landing.html')


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            print('Success!')
            return response
    form = LoginForm()
    return render(request, 'readme/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if (True):
            print(form)
            form.save()
            print('Success')
            return redirect('login')
    print('Failed')
    form = RegisterForm()
    return render(request, 'readme/register.html', {'form': form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response


def profile(request):
    return render(request, 'readme/profile.html')
