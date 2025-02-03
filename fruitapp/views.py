from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.core.paginator import Paginator
from  django.core.mail import send_mail
from django.contrib import messages
# Create your views here.



# ************************************  ABOUT  ********************************************* 
def about(request):    
    if "email" in request.session:
        return render(request,"about.html")
    else:
        return render(request,"login.html")


# ************************************  CART  ********************************************* 


def cart(request):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        print(uid)
        pid=add_to_cart.objects.filter(register=uid,order_status=False).order_by("-id")
       
        caid=user_coupon.objects.filter(user=uid,status=True).order_by("-id").first()
        if pid.count() == 0 and caid != None:
            caid.status=False
            caid.save() 

        l1=[]
        subtotal=0
        discount= 0
        shipping = 40
        total= 0
        for i in pid:
            l1.append(i.total)
        print(l1)

        if caid != None:
            discount=caid.coupon.discount

        subtotal=sum(l1)
        total=subtotal+shipping-discount
        contaxt={
            "pid":pid,
            "l1":l1,
            "subtotal":subtotal,
            "shipping": shipping,
            "total" : total,
            "discount": discount
            

        }
        return render(request,"cart.html",contaxt)
    else:
        return render(request,"login.html")
    


def cart_add(request,id):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        
        spid=product.objects.get(id=id)
        print(spid.product_name)
        print(spid.price)
        weid=add_to_cart.objects.filter(register=uid,product=spid).exists()
        print(weid)
        if weid:
            weid=add_to_cart.objects.get(register=uid,product=spid)
            weid.delete()
            return redirect(shop)
        
        add_to_cart.objects.create(register=uid,product=spid,product_name=spid.product_name,price=spid.price,quantity=1,total=spid.price,image=spid.image)

        

        return redirect(cart)
    else:    
        return render(request,"login.html")
    

def cart_minus(request,id):

    seid=add_to_cart.objects.get(id=id)
    if seid.quantity >1:
        seid.quantity-=1
        seid.total=seid.price*seid.quantity
        seid.save() 
    else:
        seid.delete()
    return redirect(cart)

def cart_plus(request,id):

    seid=add_to_cart.objects.get(id=id)
    seid.quantity+=1
    seid.total=seid.price*seid.quantity

    seid.save() 
    return redirect(cart)

def cart_delete(request,id):

    seid=add_to_cart.objects.get(id=id)
   
    seid.delete() 
    return redirect(cart)


# ************************************  CHECKOUT  ********************************************* 


import string
import razorpay

def checkout(request):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        pid=add_to_cart.objects.filter(register=uid,order_status=False).order_by("-id")
        addid=checkout_page.objects.filter(register=uid)
        caid=user_coupon.objects.filter(user=uid,status=True).order_by("-id").first()

        l1=[]
        subtotal=0
        discount=caid.coupon.discount
        shipping = 40
        total= 0
        for i in pid:
            l1.append(i.total)
        
        if caid != None:
            discount=caid.coupon.discount
        subtotal=sum(l1)
        total=subtotal+shipping-discount
        

        if request.POST:
            address_id=request.POST['options']
            aid=checkout_page.objects.get(id=address_id)
            order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            order_obj = order.objects.create(order_id=order_id,user=uid, address=aid)
            order_obj.product.set(pid)
            order_obj.total=sum(i.total for i in pid) 
            order_obj.save()
            for i in pid:
                i.order_status=True
                i.save()
        
        oid=order.objects.filter(user=uid)
        print(oid)
        for i in oid:
            print(i.datetime)
            for n in i.product.all():
                print(n.total)  
        amount = total*100 #100 here means 1 dollar,1 rupree if currency INR
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
        print(response,"")    
        if pid.count() == 0:
            shipping=0
            subtotal=0
            discount=0
            total=0

        pro={
            "uid":uid,
            "pid":pid,
            "l1": l1,
            "subtotal": subtotal,
            "shipping" :shipping,
            "discount": discount,
            "total":total,
            "addid":addid,
            "amount":amount,
            "response":response,
            "caid":caid
        }
        return render(request,"checkout.html",pro)
    else:
        return render(request,"login.html")
    


def add_address(request):
    uid=register.objects.get(email=request.session['email'])
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        address=request.POST['address']
        message=request.POST['message']
        phone=request.POST['phone']
        checkout_page.objects.create(register=uid,name=name,email=email,address=address,message=message,phone=phone)
    return redirect(checkout)


def edit_address(request,id):
    aid=checkout_page.objects.get(id=id)
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        address=request.POST['address']
        message=request.POST['message']
        phone=request.POST['phone']
        aid.name=name
        aid.email=email
        aid.address=address
        aid.message=message
        aid.phone=phone
        aid.save()
    return redirect(checkout)    


def delete_address(request,id):
    aid=checkout_page.objects.get(id=id)
    aid.delete()
    return redirect(checkout) 



# ************************************  CONTACT  ********************************************* 


def contact(request):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])

        print(uid.email)

        if request.POST:
            name=request.POST["name"]
            email=request.POST["email"]
            phone=request.POST["phone"]
            subject=request.POST["subject"]
            message=request.POST["message"]

            print(name,email,phone,subject,message)
            contect_message.objects.create(name=name,email=email,phone=phone,subject=subject,message=message)

        contaxt={
            "uid":uid
        }

        return render(request,"contact.html",contaxt)
    else:
        return render(request,"login.html")



# ************************************  INDEX  ********************************************* 


def index(request):
    if "email" in request.session:
        uid=product.objects.all()
        contaxt={
            "uid":uid
        }
        return render(request,"index.html",contaxt)
    else:
         return render(request,"login.html")


# ************************************  NEWS  ********************************************* 


def news(request):
    if "email" in request.session:
        return render(request,"news.html")
    else:
         return render(request,"login.html")
    


# ************************************  WISHLIST  ********************************************* 


def wishlist(request):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        print(uid)
        pid=wishlist_add.objects.filter(register=uid).order_by("-id")

        
        contaxt={
            "pid":pid
        }
        return render(request,"wishlist.html",contaxt)
    else:
        return render(request,"login.html")
    
     
def add_wishlist(request,id):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        spid=product.objects.get(id=id)
        print(spid.product_name)
        print(spid.price)
       
        weid=wishlist_add.objects.filter(register=uid,product=spid).exists()
        print(weid)
        if weid:
            weid=wishlist_add.objects.get(register=uid,product=spid)
            weid.delete()
            return redirect(shop)

        else:

            wishlist_add.objects.create(register=uid,product=spid,product_name=spid.product_name,price=spid.price,image=spid.image)

            return redirect(wishlist)
    else:
        return render(request,"login.html")
    
    
def wishlist_delete(request,id):

    seid=wishlist_add.objects.get(id=id)
    seid.delete() 
    return redirect(wishlist)
    

    

# ************************************  SHOP  ********************************************* 


def shop(request):
    if "email" in request.session:
        pid=product.objects.all()
        
        uid=register.objects.get(email=request.session['email'])
        wid=wishlist_add.objects.filter(register=uid).order_by("-id")
        l1=[]
        for i in wid:
            l1.append(i.product.id)
        print(l1)    

        paginator=Paginator(pid,3)
        page_get=request.GET.get("page")
        pid=paginator.get_page(page_get)

        pro={
            "pid":pid,
            "l1":l1
    
        }
        return render(request,"shop.html",pro)
    else:
         return render(request,"login.html")
    


# ************************************  SINGLE_NEWS  ********************************************* 


def single_news(request):
    if "email" in request.session:
        return render(request,"single_news.html")
    else:
         return render(request,"login.html")
    


# ************************************  SINGLE_PRODUCT  ********************************************* 


def single_product(request,id):
    if "email" in request.session:
        spid=product.objects.get(id=id)
        contaxt={
            "spid":spid
        }
        return render(request,"single_product.html",contaxt)
    else:
         return render(request,"login.html")
    


# ************************************  REGISTER_FROM  ********************************************* 

def register_from(request):
    if request.POST:
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        uid=register.objects.filter(email=email).exists()
        if uid:
            
            contaxt={
                "name":username,
                "password":password,
                "cp":confirm_password,
                "msg":"Invalid Email"
            }   
            return render(request,"register_from.html",contaxt)
        else:
            if password==confirm_password:
                print(username,email,password,confirm_password)
                register.objects.create(username=username,email=email,password=password,confirm_password=confirm_password)
                return redirect(login)
            else:
                print("error")
                return render(request,"register_from.html")
    else:
        return render(request,"register_from.html")



# ************************************  LOGIN  ********************************************* 

def login(request):
    if "email" in request.session:
        return redirect(index)
    else:

        if request.POST:
            email=request.POST["email"]
            password=request.POST["password"]       
            try:
                
                uid=register.objects.get(email=email) 
                
                if password==uid.password:
                    request.session["email"]=email
                    return redirect(index)
                else:
                    print("invalide password")
                    contaxt={
                        "pmsg":"invalide password",
                        "email":email,
                        
                        
                    }
                    return render(request,"login.html",contaxt)

            except:
                print("ok")
                print(email,password)
                contaxt={
                    "msg":" invalide email",
                    "email":email,
                    "password":password,
                    
                }
                return render(request,"login.html",contaxt)
            
            
        else:  
            return render(request,"login.html")
        

# ************************************  LOGOUT  ********************************************* 

def logout(request):
    del request.session['email']
    return redirect(login)


# ************************************  FORGATE_PASSWORD  ********************************************* 


import random
def forgate_password(request):
        if request.POST:
            email=request.POST["email"]
            otp=random.randint(1000,9999)
            uid=register.objects.filter(email=email).exists()
            print(uid)
            if uid:
                uid=register.objects.get(email=email)
                uid.otp=otp 
                uid.save()
                send_mail("test",f"test email================{otp}","gohiljayb10@gmail.com",[email])
                co={
                    "uid" : uid,

                } 
                return render(request,"confirm_password.html",co)
            else:
                co={
                   
                } 
                return render(request,"forgate_password.html",co)
    
        return render(request,"forgate_password.html")



# ************************************  CONFIRM_PASSWORD  ********************************************* 

def confirm_password(request):
    if request.POST:
        email=request.POST["email"]
        otp=request.POST["otp"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        uid=register.objects.get(email=email)
        if uid.otp == int(otp):
            print("Yes")
            if password == confirm_password:
                uid.password =password
                uid.confirm_password = confirm_password
                uid.save()
                return redirect (login)
            else:
                contaxt={
                "msg" : "invalid password",
                "uid":uid
            }
            return render(request,"confirm_password.html",contaxt)

        else:
            print("No")
            contaxt={
                "msg" : "invalid otp",
                "uid":uid
            }
            return render(request,"confirm_password.html",contaxt)



# ************************************  PROFILE  ********************************************* 


def profile(request):
    if "email" in request.session:
        uid=register.objects.get(email=request.session['email'])
        print(uid.email) 
        print(uid.username)
        if request.POST:
            username=request.POST["username"]
            s_name=request.POST["s_name"]
            email=request.POST["email"]
            education=request.POST["education"]
            address=request.POST["address"]
            phone=request.POST["phone"]
            if request.FILES:
                image=request.FILES["image"]

                uid.username=username
                uid.s_name=s_name
                uid.email=email
                uid.education=education
                uid.address=address
                uid.phone=phone
                uid.image=image
                uid.save()
            else:
                uid.username=username
                uid.s_name=s_name
                uid.email=email
                uid.education=education
                uid.address=address
                uid.phone=phone
                uid.save()


            print(username,s_name,email,education,address,phone)
        contaxt={
            "uid":uid
        }   
        return render(request,"profile.html",contaxt)
    else:
        return render(request,"login.html")




# ************************************  SEARCH  ********************************************* 


def search(request):
    if request.POST:
        search=request.POST["search"]
        print(search)
        pid=product.objects.filter(product_name__contains=search)
        contaxt={
            "pid":pid
        }
        return render(request,"shop.html",contaxt)
    


# ************************************  REVIEW  ********************************************* 
 


def review(request):
    
    if request.POST:
        rating=request.POST["rating"]
        comments=request.POST["comments"]
        
        print(rating,comments)
        user_review.objects.create(rating=rating,comments=comments)
        return redirect(index)
    return render(request,"rating.html")


# ************************************  COUPAN  ********************************************* 


def coupan(request):
    uid=register.objects.get(email=request.session['email'])
    if request.POST:
        coupon_code=request.POST["coupon_code"]

        print(coupon_code)
        cid=coupon.objects.filter(coupon_code=coupon_code).exists()
        if cid:
            print("yes")
            cide=user_coupon.objects.filter(user=uid,coupon__coupon_code=coupon_code).exists()
            if cide:
                messages.success(request, "Coupon Arlady Exists")
                return redirect(cart)
            else:
                cid=coupon.objects.get(coupon_code=coupon_code)
                user_coupon.objects.create(user=uid,coupon=cid,status=True)
                return redirect(cart)
        else:
            messages.success(request, "Coupon not Exists")
            return redirect(cart)
            
    else:

        return render(request,"cart.html")        



# ************************************  SINGLE_ORDER  ********************************************* 


def single_order(request,id):
    uid=register.objects.get(email=request.session['email'])
    caid=user_coupon.objects.filter(user=uid,status=True).order_by("-id").first()
    od=order.objects.get(order_id=id)
    discount=0
    ship=40
    if caid == None:
        discount=0
    else:
        discount=caid.coupon.discount    

    co={
        "od":od,
        "caid":caid,
        "ship":ship,
        "discount":discount,
        "total":od.total-discount+ship
    }
    return render(request,"single_order.html",co)




# ************************************  ALL_ORDER  ********************************************* 

def all_order(request):

    uid=register.objects.get(email=request.session['email'])   
    
    odr=order.objects.filter(user=uid)
    co={
        "odr":odr,
    }
    return render(request,"all_order.html",co)
    