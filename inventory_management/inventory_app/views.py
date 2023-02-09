from django.shortcuts import render

# from .forms import SignUpForm

# Create your views here.
def index(request):
    return render(request, "index.html")

def signupPage(request):
    return render(request, "signup.html")


def loginPage(request):
    return render(request, "login.html")
