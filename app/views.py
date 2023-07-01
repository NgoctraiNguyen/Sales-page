from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer= customer, complete= False)
        cartitems = order.get_cart_items
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartitems': cartitems}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'app/cart.html', context) 

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id= productId)
    order, create = Order.objects.get_or_create(customer= customer, complete= False)
    orderItem, create = OrderItem.objects.get_or_create(order= order, product= product)
    if action == 'add':
        orderItem.quantily += 1
    elif action == 'remove':
        orderItem.quantily -= 1
    orderItem.save()
    if orderItem.quantily <=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.info(request, 'User or password not corect!')

    context = {}
    return render(request, 'app/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')