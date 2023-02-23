from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("index",views.index,name="index"),
    path("cart/",views.Cart,name="Cart"),
    path("profile/",views.profile,name="profile"),
    path("getdatax/",views.Search,name="Search"),
    path("serch?<str:pk>/",views.serchview,name="serchview"),
    path("",views.LoginPage,name="LoginPage"),
    path("register/",views.RegisterPage,name="RegisterPage"),
    path("registeration/",views.register,name="register"),
    path("login/",views.Login,name="Login"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("update_cart/",views.update_cart,name="update_cart"),
    path("profileupdate/",views.profileupdate,name="profileupdate"),
    path("address/",views.address,name="addaddress"),
    path("add_address/",views.add_address,name="add_address"),
    path("CheckOut/",views.CheckOut,name="CheckOut"),
    path("checkoutpage/",views.checkoutpage,name="checkoutpage"),
    path("orderpage/",views.orderpage,name="orderpage"),    
]
