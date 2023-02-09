from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# from .forms import SignUpForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        if pass1 != pass2:
            return HttpResponse("Your passwords do not match")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect("login")

    return render(request, "signup.html")


def loginPage(request):
    if request.method == "POST":
        username1 = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=username1, password=pass1)

        if user is not None:
            login(request, user)
            print("HIeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return redirect("index")

        else:
            return HttpResponse("Username or password is incorrect")

    return render(request, "login.html")


def logoutPage(request):
    logout(request)
    return redirect("login")


def products(request, category):
    Products = Product.objects.all()
    specificProducts = {}
    for i in Products:
        print(i)
        if i.category == category:
            specificProducts += i

    return render(request, "products.html", {"products": Products})


def categories(request):
    # return render(request, "categories.html")
    productCategories = ProductCategorie.objects.all()
    return render(request, "categories.html", {"categories": productCategories})
