# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.forms.utils import ErrorList
# from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, ProfileForm
# from app.variables import *


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            profile_form = ProfileForm(request.POST, instance=user.profile)
            if profile_form.is_valid():
                profile_form.save()
                msg = 'User created.'
                success = True
            else:
                msg = 'User created but no institute associated'
                success = True
            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
            form = SignUpForm()
            profile_form = ProfileForm()

    else:
        form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, "accounts/register.html",
                  {"form": form, "profile_form": profile_form, "msg": msg, "success": success})
