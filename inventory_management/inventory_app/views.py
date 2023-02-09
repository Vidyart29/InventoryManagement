from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from .forms import SignUpForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "index.html")

def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1 = request.POST.get("pass")
        print(username, username=username, paswword=pass1 )
        if User is not None:
            login(request, User)
            return redirect('home')
    return render(request, "login.html")
