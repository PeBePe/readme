from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from readme.forms import RegisterForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError, BadRequest

import datetime


@login_required(login_url='/landing-page', redirect_field_name=None)
def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'readme/index.html', context=context)


def landing(request):
    return render(request, 'readme/landing.html')


@require_http_methods(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            if (len(username) == 0 or len(password) == 0):
                raise BadRequest()
            user = authenticate(request, username=username, password=password)
            if (user is None):
                raise ValidationError(
                    'You have entered incorrect username or password')
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        except ValidationError as err:
            return render(request, 'readme/login.html', {'form': form, 'error': err.message})
        except BadRequest as err:
            return render(request, 'readme/login.html', {'form': form})
    else:
        return render(request, 'readme/login.html')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            form.save()
            return redirect('login')
        except:
            return render(request, 'readme/register.html', {'form': form})
    else:
        return render(request, 'readme/register.html')


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response


def profile(request):
    return render(request, 'readme/profile.html')
