from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('cart/', views.cart, name= 'cart'),
    path('chechout/', views.checkout, name= 'checkout'),
    path('update_item/', views.updateItem, name= 'update_item'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('search/', views.search, name= 'search'),
    path('category', views.category, name='category'),
    path('detailproduct/', views.detailproduct, name= 'detailproduct'),
]