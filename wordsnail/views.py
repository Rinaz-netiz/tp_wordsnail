from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterUserForm



__all__ = (
    "home",
    "register",
)


def home(request):
    return render(request, "wordsnail/home.html")


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            redirect("/")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterUserForm()
    return render(request, "registration/register.html", {'form': form})




