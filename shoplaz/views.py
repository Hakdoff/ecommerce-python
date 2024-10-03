from itertools import product

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, AddtoCart
from django.contrib import messages

from .models import Product, Cart


def home(request):
    return render(request, 'home.html', {'products': Product.objects.all()})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}')
            return redirect(home)
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid Credentials')
            return redirect('login_user')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, f'You are now logged out')
    return redirect('home')


def products(request, pk):
    products = Product.objects.get(id=pk)
    form = AddtoCart(initial={'product_id': pk})
    return render(request, 'products.html', {'products': products, 'form': form})


def add_to_cart(request, product_id):
    form = None
    if request.method == 'POST':
        products = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(
                product_id=products, user_id=request.user,
                defaults={'quantity': 1})

            if not created:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, f'Your cart {products.product_name} has been updated')
            else:
                messages.success(request, f'Your cart {products.product_name} has been added')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.success(request, f'Please login before adding to cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        form = AddtoCart(initial={'product_id': product_id})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user_id=request.user)
    else:
        carts = []
    return render(request, 'cart.html', {'carts': carts, 'products': Product.objects.all()})

