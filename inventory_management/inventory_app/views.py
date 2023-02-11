from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .email import sendMail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from threading import Thread
import datetime
import uuid
from django.contrib import messages

# from .forms import SignUpForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "base.html")


@login_required(login_url="login")
def profile(request):
    context = {}

    if request.user.is_authenticated:
        # Get all completed orders for current logged in user
        customer = request.user
        orders = Order.objects.filter(customer=customer, complete=True)

        # Construct a list of orders as a list of dictionaries
        orderList = []
        for order in orders:
            items = order.orderitem_set.all()

            itemsInOrder = []
            for item in items:
                totalCost = item.quantity * item.product.price
                itemsInOrder.append(
                    str(item.product.productName + " : " + str(item.quantity))
                )

            # Construct a dictionary for every orders' attributes
            oneOrder = {
                "transaction_id": order.transaction_id,
                "buCode": order.buCode,
                "date": str(order.date_ordered),
                "itemsInOrder": itemsInOrder,
                "noOfItems": int(len(items)),
                "totalCost": totalCost,
            }

            orderList.append(oneOrder)

    # Reverse the list so that new orders come up first
    context = {"orders": orderList[::-1]}

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

    # Doesn't allow an already authenticated user to go to signup page
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "signup.html")


def loginPage(request):
    if request.method == "POST":
        username1 = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=username1, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("products")

        else:
            return HttpResponse("Username or password is incorrect")

    # Doesn't allow an already authenticated user to go to signup page
    if request.user.is_authenticated:
        return redirect("home")
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
        Products = Product.objects.filter(category__name__contains=cat, disabled=False)
    else:
        # print("hi")
        cat = "All Products"
        Products = Product.objects.filter(disabled=False)
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
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    if request.method == "POST":
        bu_code = request.POST.get("bucode")
        # Check if there are enough items in stock
        notEnough = []
        for item in items:
            if item.quantity <= item.product.quantity:
                enoughInventory = True
            else:
                enoughInventory = False
                notEnough.append(
                    {
                        "productName": item.product.productName,
                        "requestedQuantity": item.quantity,
                        "availableQuantity": item.product.quantity,
                    }
                )

        if enoughInventory:
            # Remove the items from inventory
            item.product.quantity -= item.quantity
            item.product.save()

            # Set transaction id and bu_code
            transaction_id = str(uuid.uuid4())[:8]
            order.transaction_id = transaction_id
            order.buCode = bu_code

            # Set the order to complete and save
            order.complete = True
            order.date_ordered = datetime.datetime.now()
            order.save()

            # Util logic
            myitems = []
            for i in items:
                myitems.append(str(i))
                totalCost = i.quantity * i.product.price

            # Email logic
            email = request.user.email
            thread = Thread(target=sendMail, args=(email, order, myitems, totalCost))
            thread.start()

            messages.success(request, "Order Placed Successfully")
            context = {
                "order": order,
                "myitems": myitems,
                "totalCost": totalCost,
                "successful": True,
            }
            return render(request, "checkout.html", context)
            # return HttpResponse("Checked out successfully")
        else:
            context = {
                "order": None,
                "myitems": None,
                "totalCost": None,
                "successful": False,
                "item": notEnough,
            }
            return render(request, "checkout.html", context)

    context = {}
    context = {"items": items, "order": order}
    return render(request, "cart.html", context)
