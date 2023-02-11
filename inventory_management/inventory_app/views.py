from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
from .email import sendMail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from threading import Thread

# from .forms import SignUpForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "base.html")


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
    # print("ghhghghgh")
    if request.method == "POST":
        username1 = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=username1, password=pass1)

        # print(user)
        if user is not None:
            login(request, user)
            # print("HIeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return redirect("products")

        else:
            return HttpResponse("Username or password is incorrect")

    return render(request, "login.html")


def logoutPage(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def products(request, cat="None"):
    # id = ProductCategorie.objects.filter(category__name="Laptop")
    # Products = Product.objects.filter(category__name__contains="Laptops")
    # print("cat ", type(cat))
    if cat != "None":
        Products = Product.objects.filter(category__name__contains=cat)
    else:
        # print("hi")
        cat = "All Products"
        Products = Product.objects.all()
    print(Products)
    return render(request, "products.html", {"products": Products, "cat": cat})


@login_required(login_url="login")
def categories(request):
    # return render(request, "categories.html")
    productCategories = ProductCategorie.objects.all()
    return render(request, "categories.html", {"categories": productCategories})


@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data["productId"]
    action = data["action"]

    print("aciton: ", action)
    print("prouct: ", productId)

    # print(request)
    customer = request.user
    print(customer)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def send_email(request):
    # email= request.POST['email']
    # bucode= request.POST['bucode']
    sendMail("vidya.rautela.28@gmail.com", "bucode")

    return HttpResponse("Submitted")


def email(request):
    return render(request, "email.html")


@login_required(login_url="login")
def cart(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}

    context = {"items": items, "order": order}
    # print("11111111111111111111                      ", customer)

    if request.method == "POST":

        # condition will be enough items in inventory
        condition = True
        if condition:
            content = request.POST.get("bucode")
            email = request.user.email
            thread = Thread(target=sendMail, args=(email, content))
            thread.start()
            # sendMail("dsouzajenslee@gmail.com", "hiiiiiiiiiiiiiii")
            return HttpResponse("Checked out successfully")
        else:
            return HttpResponse("No Stock Available")

    return render(request, "cart.html", context)


# def checkout(request):
#     context = {}

#     if request.user.is_authenticated:
#         customer = request.user.id
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#     else:
#         items = []
#         order = {"get_cart_total": 0, "get_cart_items": 0}

#     context = {"items": items, "order": order}

#     # condition will be for inventory stock checking
#     if request.method == "POST":
#         condition = True
#         if condition:
#             # content = request.post.get("bucode")
#             # thread = Thread(target=sendMail, args=(content))
#             sendMail("dsouzajenslee@gmail.com", "hiiiiiiiiiiiiiii")
#             return HttpResponse("Checked out successfully")
#         else:
#             return HttpResponse("No Stock Available")
#     else:
#         return render(request, "checkout.html", context)
