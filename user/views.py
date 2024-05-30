from django.shortcuts import render
from user.forms import SignUpForm, LoginForm

from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as user_login, authenticate
# Create your views here.

def signup(request):
    form = SignUpForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("email")
            messages.success(request, f"Account created for {username}!")
            return HttpResponseRedirect(reverse("index"))
        messages.error(request, "Please enter valid data!")
        return render(request, "user/signup.html", {"form": form})
    context = {

        "form":SignUpForm()
    }
    return render(request, "user/signup.html", context)

def login(request):
    #form = LoginForm(request.POST or None)
    form = LoginForm(data=request.POST)
    if request.method == "POST":
        print(form)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request, "Login successful!")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "please enter valid data123")
                return HttpResponseRedirect(reverse("user:login"))
        messages.error(request, "please enter valid data321")
        return HttpResponseRedirect(reverse("user:login"))
    return render(request, "user/login.html",{"form":form})