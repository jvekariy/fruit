"""
URL configuration for fruitproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fruitapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('cart_add/<int:id>', views.cart_add, name='cart_add'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('news', views.news, name='news'),
    path('shop', views.shop, name='shop'),
    path('single_news', views.single_news, name='single_news'),
    path('single_product/<int:id>', views.single_product, name='single_product'),
    path('register_from', views.register_from, name='register_from'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('confirm_password', views.confirm_password, name='confirm_password'),
    path('forgate_password', views.forgate_password, name='forgate_password'),
    path('add_wishlist/<int:id>', views.add_wishlist, name='add_wishlist'),
    path('wishlist_delete/<int:id>', views.wishlist_delete, name='wishlist_delete'),
    path('cart_delete/<int:id>', views.cart_delete, name='cart_delete'),
    path('review', views.review, name='review'),
    path('rating', views.rating, name='rating'),

    path('cart_plus/<int:id>', views.cart_plus, name='cart_plus'),
    path('cart_minus/<int:id>', views.cart_minus, name='cart_minus'),


      

]
