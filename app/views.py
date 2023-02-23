from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .models import *
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator
# Create your views here.

def LoginPage(request):
    if 'userid' in request.session:
        return redirect('index')
    else:
        contax = {
            'title' : 'Karma Shop',
        }
        return render(request, "login.html",contax)

def RegisterPage(request):
    if 'userid' in request.session:
        return redirect('index')
    else:
        contax = {
            'title' : 'Karma Shop',
        }
        return render(request, "Register.html",contax)

def index(request):
    if 'userid' in request.session:
        products = Product.objects.all()
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        product = paginator.get_page(page_number)
        totalpages = product.paginator.num_pages
        contax = {
            'title' : 'Karma Shop',
            "brands" : Brand.objects.all(),
            'Product' : product,
            'totalpages' : totalpages,
        }
        return render(request, "index.html",contax)
    else:
        return redirect('LoginPage')

def serchview(request,pk):
    if 'userid' in request.session:
        products = Product.objects.filter(productname__icontains=pk)
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        product = paginator.get_page(page_number)
        totalpages = product.paginator.num_pages
        contax = {
            'title' : 'Karma Shop',
            'inds' : 'search',
            "brands" : Brand.objects.all(),
            'Product' : product,
            'totalpages' : totalpages,
        }
        return render(request, "index.html",contax)
    else:
        return redirect('LoginPage')

def Search(request):
    if request.method == "POST":
        data = request.POST['data'].casefold()
        return redirect('serchview',data)
    else:
        return redirect('index')

def profile(request):
    if 'userid' in request.session:        
        contax = {
            'title' : 'Karma Shop',
            "brands" : Brand.objects.all(),
            'profile' : Users.objects.get(id=request.session['userid']),
            'address' : ShippingAdrress.objects.filter(user_id=request.session['userid']),
        }
        return render(request, "profile.html",contax)
    else:
        return redirect('LoginPage')

def profileupdate(request):
    if 'userid' in request.session:        
        profile = Users.objects.get(id=request.session['userid'])
        profile.firstname = request.POST['firstname'] if request.POST['firstname'] else profile.firstname
        profile.lastname = request.POST['lastname'] if request.POST['lastname'] else profile.lastname
        profile.email = request.POST['email'] if request.POST['email'] else profile.email
        profile.number = request.POST['contact_num'] if request.POST['contact_num'] else profile.number
        profile.alt_number = request.POST['alt_contact_num'] if request.POST['alt_contact_num'] else profile.alt_number
        profile.save()
        messages.success(request, f"Profile Updated Successfully")
        return redirect('profile')
    else:
        return redirect('profile')

def Cart(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        carts = cart.objects.filter(user_id=userid,status='0')
        if len(carts) > 0:
            subtotal = 0
            for i in carts:
                subtotal = subtotal + int(i.price)
            contax = {
                'title' : 'Karma Shop',
                'carts' : carts,
                'address' : ShippingAdrress.objects.filter(user_id=request.session['userid']),
                "brands" : Brand.objects.all(),
                "Subtotal" : subtotal,
                # "GST" : format((int(subtotal)*18)/ 100,'.2f') ,
                # "withGST" : format((int(subtotal)*18)/ 100 + subtotal,'.2f'),
            }
            return render(request, "cart.html",contax)
        else:
            return redirect('index')
    else:
        return redirect('LoginPage')

def address(request):
    if 'userid' in request.session:
        contax = {
            'title' : 'Karma Shop',
            "brands" : Brand.objects.all(),
        }
        return render(request, "address.html",contax)
    else:
        return redirect('LoginPage')

def add_address(request):
    if 'userid' in request.session:        
        profile = Users.objects.get(id=request.session['userid'])
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        State = request.POST['State']
        zipcode = request.POST['zipcode']
        country = request.POST['country']
        adds = ShippingAdrress.objects.create(
            user_id = profile,
            address1 = address1,
            address2 = address2,
            city = city,
            state = State,
            zipcode = zipcode,
            country = country,
        )
        messages.success(request, f"Add Address Successfully")
        return redirect('profile')
    else:
        return redirect('profile')

def register(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if(not email):
            messages.error(request, f"Username Required!")
            return redirect("RegisterPage")
        if(not password):
            messages.error(request, f"Password Required!")
            request.session['username'] = email
            return redirect("RegisterPage")
        if(not cpassword):
            messages.error(request, f"Confirm Password Required!")
            request.session['username'] = email
            return redirect("RegisterPage")

        if cpassword != password:
            request.session['username'] = email
            messages.error(request, f"Password Don't Match")
            return redirect('RegisterPage')
        else:
            users = Users.objects.filter(email=email)
            if len(users) > 0:
                request.session['username'] = email
                messages.error(request, f"User Already Register Please Login")
                return redirect('LoginPage')
            else:
                users = Users.objects.create(
                    email = email,
                    password = make_password(password),
                    cpassword = cpassword,
                )
                request.session['username'] = email
                messages.success(request, f"User Register Successfully Please Login Here")
                return redirect('LoginPage')
    else:
        return redirect('RegisterPage')

def Login(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']
        
        if(not email):
            messages.error(request, f"Username Required!")
            return redirect('LoginPage')
        if(not password):
            messages.error(request, f"Password Required!")
            request.session['username'] = email
            return redirect('LoginPage')
        
        users = Users.objects.filter(email=email)
        if len(users)>0:
            pas = check_password(password, users[0].password)
            if pas:
                if 'username' in request.session:
                    del request.session['username']
                request.session['userid'] = users[0].id
                return redirect('index')
            else:
                request.session['username'] = email
                messages.error(request, f"Password Wrong")
                return redirect('LoginPage')
        else:
            messages.error(request, f"User Doesn't Found Please Register")
            return redirect('RegisterPage')
    else:
        return redirect('LoginPage')

def Logout(request):
    if 'userid' in request.session:
        del request.session['userid']
        return redirect('LoginPage')
    else:
        return redirect('LoginPage')
   
def addtocart(request):
    if request.method == "POST":
        userid = request.session['userid']
        id = request.POST.get('pid')
        carts = cart.objects.filter(product_id=id,user_id=userid,status='0')
        if len(carts) > 0:
            carts[0].qty = int(carts[0].qty) + 1
            carts[0].price = int(carts[0].price) + int(carts[0].product_id.product_price)
            carts[0].save()
        else:
            pid = Product.objects.get(id=id)
            user_id = Users.objects.get(id=userid)
            carts = cart.objects.create(
                product_id=pid,
                qty = 1,
                user_id = user_id,
                price = pid.product_price,
            )
        return JsonResponse({'status' : '1'})
    else:
        return JsonResponse({'status' : '0'})

def update_cart(request):
    if request.method == "POST":
        id = request.POST.get('pid')
        userid = request.session['userid']
        qty = request.POST.get('qty')
        carts = cart.objects.get(id=id)
        carts.qty = qty
        carts.price = int(qty) * int(carts.product_id.product_price)
        carts.save()
        allcarts = cart.objects.filter(user_id=userid)
        subtotal = 0
        for i in allcarts:
            subtotal = int(i.price) + subtotal
        return JsonResponse({'status' : '1',"update_price":carts.price,"subtotal":subtotal})
        # return JsonResponse({'status' : '1',"update_price":carts.price,"subtotal":subtotal, "GST" : format((int(subtotal)*18)/ 100,'.2f'),"withGST" : format((int(subtotal)*18)/ 100 + subtotal,'.2f'),})
    else:
        return JsonResponse({'status' : '0'})

def checkoutpage(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        carts = cart.objects.filter(user_id=userid,status='0')
        if len(carts) > 0:
            subtotal = 0
            for i in carts:
                subtotal = subtotal + int(i.price)
            contax = {
                'title' : 'Karma Shop',
                'carts' : carts,
                'useremail' : Users.objects.get(id=userid),
                'address' : ShippingAdrress.objects.filter(user_id=request.session['userid']),
                "brands" : Brand.objects.all(),
                "Subtotal" : subtotal,
                "GST" : format((int(subtotal)*18)/ 100,'.2f') ,
                "withGST" : format((int(subtotal)*18)/ 100 + subtotal,'.2f'),
            }
            return render(request, "Checkout.html",contax)
        else:
            return redirect('index')
    else:
        return redirect('LoginPage')

def orderpage(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        contax = {
            'title' : 'Karma Shop',
            "brands" : Brand.objects.all(),
            "order" : order.objects.filter(user_id = userid),
        }
        return render(request, "order.html",contax)
    else:
        return redirect('LoginPage')

def CheckOut(request):
    if request.method == "POST":
        user_id = request.session['userid']
        userid = Users.objects.get(id=user_id)

        first = request.POST.get('first')
        last = request.POST.get('last')
        company = request.POST.get('company')
        number = request.POST.get('number')
        email = request.POST.get('email')
        country = request.POST.get('country')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zip')
        price = request.POST.get('price')

        id = request.POST.get('address_id')
        if(not id):
            if(not country) or (not add1) or (not state) or (not city):
                return JsonResponse({'status' : '2'})
            adds = ShippingAdrress.objects.create(
                user_id = userid,
                address1 = add1,
                address2 = add2,
                city = city,
                state = state,
                zipcode = zipcode,
                country = country,
            )
            id = adds

        add_id = ShippingAdrress.objects.get(id=id)
        carts = cart.objects.filter(user_id=userid,status='0')
        if len(carts) > 0:
            orders = order.objects.create(
                firstname = first,
                companyname = company,
                lastname = last,
                email = email,
                number = number,
                user_id = userid,
                address = add_id,
                price = price,
            )
            for i in carts:
                i.status = "1"
                i.save()
                orders.cart_id.add(i.id)
                orders.save()
            return JsonResponse({'status' : '1',"msg":"order Successfull"})
            messages.success(request, f"Thank you. Your order has been received.")
        else:
            return JsonResponse({'status' : '3'})
    else:
        return JsonResponse({'status' : '0'})

