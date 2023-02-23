from django.db import models

# Create your models here.

class Users(models.Model):
    firstname = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    number = models.CharField(max_length=255,blank=True,null=True)
    alt_number = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    cpassword = models.CharField(max_length=255,blank=True,null=True)

class ShippingAdrress(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,blank=True)
    address1 = models.CharField(max_length=255,blank=True,null=True)
    address2 = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=255,blank=True,null=True)
    country = models.CharField(max_length=255,blank=True,null=True)

class Brand(models.Model):
    brand_name = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.brand_name

class Product(models.Model):
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True,blank=True)
    productname = models.CharField(max_length=255,blank=True,null=True)
    product_price = models.CharField(max_length=255,blank=True,null=True)
    product_MRP = models.CharField(max_length=255,blank=True,null=True)
    product_image = models.ImageField(upload_to="products_image/",height_field=None, width_field=None, max_length=255,blank=True,null=True) 
    product_stock = models.CharField(max_length=255,blank=True,null=True)

class cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,blank=True)
    qty = models.CharField(max_length=255,blank=True,null=True)
    price = models.CharField(max_length=255,blank=True,null=True)
    status = models.CharField(max_length=255,blank=True,null=True,default='0',choices=[('1','Order'),('0','Not_order')])

class order(models.Model):
    firstname = models.CharField(max_length=255,blank=True,null=True)
    companyname = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    number = models.CharField(max_length=255,blank=True,null=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,blank=True)
    cart_id = models.ManyToManyField(cart)
    address = models.ForeignKey(ShippingAdrress, on_delete=models.CASCADE,null=True,blank=True)
    price = models.CharField(max_length=255,blank=True,null=True)
    status = models.CharField(max_length=255,blank=True,null=True,default='0',choices=[('0','Pending'),('1','Accept'),('2','Reject')])