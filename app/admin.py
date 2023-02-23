from django.contrib import admin
from .models import *

# Register your models here.
class Productadmin(admin.ModelAdmin):
    # model =Product
    list_per_page = 15 # No of records per page 
    list_display = ('productname','brand_id','product_price','product_MRP','product_image','product_stock')
    list_display_links = ('productname','brand_id','product_price','product_MRP','product_image','product_stock')
    ordering = ('-id'),

class Brandadmin(admin.ModelAdmin):
    # model =Brand
    list_per_page = 15 # No of records per page 
    list_display = ('brand_name',)
    list_display_links = ('brand_name',)
    ordering = ('-id'),

class Usersadmin(admin.ModelAdmin):
    # model =Users
    list_per_page = 15 # No of records per page 
    list_display = ('firstname','lastname','email','number','alt_number','cpassword')
    list_display_links = ('firstname','lastname','email','number','alt_number','cpassword')
    ordering = ('-id'),

class orderadmin(admin.ModelAdmin):
    # model =order
    list_per_page = 15 # No of records per page 
    list_display = ("firstname","lastname","companyname","price","status")
    list_display_links = ("firstname","companyname","lastname","price")
    list_editable  = ("status",)
    ordering = ('-id'),

admin.site.register(Product,Productadmin)
admin.site.register(Brand,Brandadmin)
admin.site.register(Users,Usersadmin)
admin.site.register(order,orderadmin)