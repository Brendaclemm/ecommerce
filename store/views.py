from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def all_categories():
    categories = Category.objects.all()
    return categories


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {'products': products, 'categories': all_categories()})


def category(request, foo):
    # replace spaces with hyphens
    # foo = foo.replace(' ', '_')

    # grab category from the url
    try:
        # look up category
        product_category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=product_category)
        return render(request, "store/category.html", {'products': products, 'category': product_category, 'categories': all_categories()})
    except:
        messages.success(request, "There is no such category")
        return redirect('home')


def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "store/product.html", {'product': product})


def about(request):
    return render(request, "store/about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error")
            return redirect('login')

    else:
        return render(request, 'store/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully")
            return redirect('home')
        else:
            messages.success(request, "There was a problem. Please try again")
            return redirect('register')

    return render(request, 'store/register.html', {'form': form})
