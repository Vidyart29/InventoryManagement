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
import datetime
import uuid

# from .forms import SignUpForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "base.html")


@login_required(login_url="login")
def profile(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user
        orders = Order.objects.filter(customer=customer, complete=True)
        # items = order.orderitem_set.all()
        # print(items)
        orderList = []
        for order in orders:
            # print(i.transaction_id)
            items = order.orderitem_set.all()
            # currOrder = {}
            # currOrder.update('transaction_id': items.)
            # orderList.append()
            # print("tid: ", order.transaction_id)
            # print("date: ", str(order.date_ordered))
            # print(
            #     "list :",
            #     [str(i.product.productName + ":" + str(i.quantity)) for i in items],
            # )
            oneOrder = {
                "transaction_id": order.transaction_id,
                "date": str(order.date_ordered),
                "itemsInOrder": [
                    str(i.product.productName + ":" + str(i.quantity)) for i in items
                ],
                "noOfItems": int(len(items)),
            }
            orderList.append(oneOrder)
            # for i in orderList:
            #     print(i)

    else:

        order = {"get_cart_total": 0, "get_cart_items": 0}
    # print()
    # print(itemList)
    context = {"orders": orderList}
    # print(context)

    return render(request, "profile.html", context)


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


@login_required(login_url="login")
def cart(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user
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
            transaction_id = uuid.uuid4()
            print("order started")
            order.complete = True
            order.transaction_id = transaction_id
            order.date_ordered = datetime.datetime.now()
            order.save()
            print(created)
            print("rder saved")

            # email logic
            content = request.POST.get("bucode")
            email = request.user.email
            thread = Thread(target=sendMail, args=(email, content))
            thread.start()
            # sendMail("dsouzajenslee@gmail.com", "hiiiiiiiiiiiiiii")
            return redirect(url_name)
        else:
            return HttpResponse("No Stock Available")

    return render(request, "cart.html", context)
