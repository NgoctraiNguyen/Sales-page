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
    categorys = Category.objects.all()
    context = {'products': products, 'cartitems': cartitems, 'categorys': categorys}
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

    categorys = Category.objects.all()
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'categorys': categorys}
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

    categorys = Category.objects.all()
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'categorys': categorys}
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
    cartitems = 0    
    categorys = Category.objects.all()
    context = {'form': form, 'categorys': categorys, 'cartitems': cartitems}
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

    cartitems = 0 
    categorys = Category.objects.all()
    context = {'categorys': categorys, 'cartitems': cartitems}
    return render(request, 'app/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')

def search(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer= customer, complete= False)
        cartitems = order.get_cart_items
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']

    if request.method == 'POST':
        key_search = request.POST.get('search')
        product_search = Product.objects.filter(name__contains = key_search)

    categorys = Category.objects.all()
    context = {'key_search': key_search, 'products': product_search, 'cartitems': cartitems, 'categorys': categorys}
    return render(request, 'app/search.html', context)

def category(request):
    category_slug = request.GET.get('category')
    category = Category.objects.filter(slug = category_slug).values_list('name', flat= True).distinct()
    products = Product.objects.filter(category__slug= category_slug)
    categorys = Category.objects.all()
    context = {'category': category[0], 'products': products, 'categorys': categorys, 'cartitems': 0}
    return render(request, 'app/category.html', context)

def detailproduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer= customer, complete= False)
        cartitems = order.get_cart_items
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']
    productId = request.GET.get('productid')
    products = Product.objects.filter(id= productId)
    context = {'products': products, 'cartitems': cartitems}
    return render(request, 'app/detailproduct.html', context)