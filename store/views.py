from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q


def all_categories():
    categories = Category.objects.all()
    return categories


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {'products': products, 'categories': all_categories()})

def category_summary(request):
    return render(request, "store/category_summary.html", {'categories': all_categories()})

def category(request, foo):
    # replace spaces with hyphens
    # foo = foo.replace(' ', '_')

    # grab category from the url
    try:
        # look up category
        product_category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=product_category)
        return render(request, "store/category.html",
                      {'products': products, 'category': product_category, 'categories': all_categories()})
    except:
        messages.success(request, "There is no such category")
        return redirect('home')


def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "store/product.html", {'product': product})


def about(request):
    return render(request, "store/about.html", {})


def search(request):
    # determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #query the products DB model
        searched_product = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        # test for null
        if not searched_product:
            messages.success(request, "Product not found!")

        return render(request, "store/search.html", {'searched':searched_product})
    else:
        return render(request, "store/search.html", {})

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
            messages.success(request, "You have registered successfully. Please fill in your user information")
            return redirect('update_info')
        else:
            messages.success(request, "There was a problem. Please try again")
            return redirect('register')

    return render(request, 'store/register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User has been updated')
            return redirect('home')
        return render(request, 'store/update_user.html', {'user_form':user_form})
    else:
        messages.success(request, 'You must be logged in to access that page')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated.')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form':form})
    else:
        messages.success(request, 'You must be logged in to change password.')
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_profile)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your user information has been updated!')
            return redirect('home')
        return render(request, 'store/update_info.html', {'form':form})
    else:
        messages.success(request, 'You must be logged in to access that page')

        return redirect('home')



