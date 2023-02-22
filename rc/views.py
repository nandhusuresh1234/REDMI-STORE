from datetime import datetime
from datetime import timedelta
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from second.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
import uuid


def shopregisterr(request):
    if request.method == 'POST':
        a = shopNregif(request.POST)
        if a.is_valid():
            sn = a.cleaned_data['uname']
            ua = a.cleaned_data['uaddress']
            si = a.cleaned_data['ushopid']
            se = a.cleaned_data['uemail']
            sp = a.cleaned_data['uphone']
            spass = a.cleaned_data['upassword']
            sconf = a.cleaned_data['upassword2']
            if spass == sconf:
                b = shopregister(uname=sn, uaddress=ua, ushopid=si, uemail=se, uphone=sp, upassword=spass,upassword2=sconf)
                b.save()
                return redirect(shoplogin1)
            else:
                return HttpResponse("Password Dosn't Match")
        else:
            return HttpResponse("Registration Failed")

    return render(request, 'shopregister.html')


def shoplogin1(request):
    if request.method == 'POST':
        a = shoploginF(request.POST)
        if a.is_valid():
            un = a.cleaned_data['uname']
            up = a.cleaned_data['upassword']
            request.session['uname']=un
            b = shopregister.objects.all()
            for i in b:
                if un==i.uname and up==i.upassword2:
                    request.session['uid']=i.id
                    return redirect(profile1)
            else:
                    return HttpResponse("failed")
    return render(request, "shoplogin.html")

def profile1(request):
    uname=request.session['uname']
    return render(request, 'profile.html',{'uname':uname})


def upload(request):
    if request.method == 'POST':
        a = uploadform(request.POST, request.FILES)
        id = request.session['uid']
        if a.is_valid():
            upn = a.cleaned_data['upname']
            upp = a.cleaned_data['upprice']
            upd = a.cleaned_data['updiscription']
            upf = a.cleaned_data['upfile']
            b = uploadmodel(shopid=id,upname=upn, upprice=upp, updiscription=upd, upfile=upf)
            b.save()
            return HttpResponse("upload success")

        else:
            return HttpResponse('upload failed')
    return render(request, 'upload.html')


def productdisplay(request):
    shop_id=request.session['uid']
    a = uploadmodel.objects.all()
    nm = []
    pr = []
    dis = []
    fil = []
    id = []
    sid=[]
    for i in a:
        id1 = i.id
        id.append(id1)

        upn = i.upname
        nm.append(upn)

        upp = i.upprice
        pr.append(upp)

        upd = i.updiscription
        dis.append(upd)

        upf = i.upfile
        fil.append(str(upf).split('/')[-1])

        s_id=i.shopid
        sid.append(s_id)

    mylist = zip(nm, pr, dis, fil, id, sid)
    return render(request, 'productdisplay.html', {'mylist': mylist,'shop_id':shop_id})


def delete(request, id):
    a = uploadmodel.objects.get(id=id)
    a.delete()
    return redirect(productdisplay)


def edit(request, id):
    a = uploadmodel.objects.get(id=id)
    im = str(a.upfile).split('/')[-1]
    if request.method == 'POST':
        if len(request.FILES):
            if len(a.upfile) > 0:
                os.remove(a.upfile.path)
            a.upfile = request.FILES['upfile']
        a.upname = request.POST.get('upname')
        a.upprice = request.POST.get('upprice')
        a.updiscription = request.POST.get('updiscription')
        a.save()
        return redirect(productdisplay)
    return render(request, 'edit.html', {'a': a, 'im': im})


def userregistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get("last_name")
        email = request.POST.get('email')
        password = request.POST.get('password')
        #     checking whether username exist
        if User.objects.filter(username=username).first():
            # it will get the first object from the filter query
            messages.success(request, "username already taken")
            # message.succes aframework that allows you to store messages in one request

            return redirect(userregistration)
        if User.objects.filter(email=email).first():
            messages.success(request, "email already exist")
            return redirect(userregistration)
        user_obj = User(username=username, email=email, first_name=firstname, last_name=lastname)
        user_obj.set_password(password)
        user_obj.save()
        # uuid==uuid that stands for universly unique indentifiers uuid creates random UUID
        auth_token = str(uuid.uuid4())
        profile_obj = profile.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email, auth_token)  # user defined function  mail sending function
        return render(request, 'success.html')
    return render(request, 'userregister.html')


def send_mail_regis(email, auth_token):  # subject ,from email, recipient
    subject = "your account has been verified"
    # f is astring literal which contains expressions inside curly brackets the expressions are replaced by values
    message = f'click the link to verify your account http://127.0.0.1:8000/new/verify/{auth_token}'
    email_from = EMAIL_HOST_USER  # from
    recipient = [email]  # to
    send_mail(subject, message, email_from, recipient)


def success(request):
    return render(request, 'success.html')


def userprofile(request):
    return render(request, 'userprofile.html')


def verify(request, auth_token):
    profile_obj = profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'your account is already verified')
            return redirect(login)
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, "your account has been verified")
        return redirect(login)
    else:
        messages.success(request, 'user not found')
        return redirect(login)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = User.objects.filter(username=username).first()
        request.session['id'] = user_obj.id
        request.session['username']=username
        if user_obj is None:
            messages.success(request, "user not found")
            return redirect(login)
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, "profile not verified check your Email")
            return redirect(login)

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, "wrong password or username")
            return redirect(login)
        return redirect(userprofile)
    return render(request, "userlogin.html")


def index(request):
    return render(request, "index.html")


def userproductdisplay(request):
    b=request.session['username']
    a = uploadmodel.objects.all()
    nm = []
    pr = []
    dis = []
    fil = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)

        upn = i.upname
        nm.append(upn)

        upp = i.upprice
        pr.append(upp)

        upd = i.updiscription
        dis.append(upd)

        upf = i.upfile
        fil.append(str(upf).split('/')[-1])

    mylist = zip(nm, pr, dis, fil, id)
    return render(request, 'userproductdisplay.html', {'mylist': mylist,'b':b})

def viewallp(request):
    a = uploadmodel.objects.all()
    nm = []
    pr = []
    dis = []
    fil = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)

        upn = i.upname
        nm.append(upn)

        upp = i.upprice
        pr.append(upp)

        upd = i.updiscription
        dis.append(upd)

        upf = i.upfile
        fil.append(str(upf).split('/')[-1])

    mylist = zip(nm, pr, dis, fil, id)
    return render(request, 'viewallproducts.html', {'mylist': mylist})


def addtocart(request, id):
    c=request.session['id']
    a = uploadmodel.objects.get(id=id)
    if cart.objects.filter(upname=a.upname):
       return HttpResponse("product is already in the cart")
    else:
        b = cart(upname=a.upname, upprice=a.upprice, updiscription=a.updiscription, upfile=a.upfile,userid=c)
        b.save()
    return redirect(userproductdisplay)
    # return render(request,"cart.html")


def addtocart1(request,id):
    c=request.session['id']
    a = wishlist.objects.get(id=id)
    b = cart(upname=a.upname, upprice=a.upprice, updiscription=a.updiscription, upfile=a.upfile,userid=c)
    b.save()
    return redirect(cartdisplay)


def cartdisplay(request):
    n=request.session['username']
    cart_id=request.session['id']
    a = cart.objects.all()
    prdname = []
    prdprice = []
    prddes = []
    prdfl = []
    id = []
    cid=[]
    for i in a:
        idd = i.id
        nm = i.upname
        ppr = i.upprice
        ds = i.updiscription
        fl = i.upfile
        cd=i.userid
        prdfl.append(str(fl).split('/')[-1])
        prdname.append(nm)
        prdprice.append(ppr)
        prddes.append(ds)
        id.append(idd)
        cid.append(cd)
    list = zip(prdfl, prdname, prdprice, prddes,id,cid)
    return render(request, 'cart.html', {'list': list,'cart_id':cart_id,'cid':cid,'n':n})


def addtowishlist(request, id):
    c=request.session['id']
    a = uploadmodel.objects.get(id=id)
    if wishlist.objects.filter(upname=a.upname):
        return HttpResponse("Product already in Wishlist")
    else:
        b = wishlist(upname=a.upname, upprice=a.upprice, updiscription=a.updiscription, upfile=a.upfile,userid=c)
        b.save()
    return redirect(wishlistdisplay)


def wishlistdisplay(request):
    s=request.session['username']
    wish_id=request.session['id']
    a = wishlist.objects.all()
    prdname = []
    prdprice = []
    prddes = []
    prdfl = []
    id = []
    wid=[]
    for i in a:
        idd = i.id
        nm = i.upname
        ppr = i.upprice
        ds = i.updiscription
        fl = i.upfile
        wd=i.userid

        prdfl.append(str(fl).split('/')[-1])
        prdname.append(nm)
        prdprice.append(ppr)
        prddes.append(ds)
        id.append(idd)
        wid.append(wd)
    list = zip(prdfl, prdname, prdprice, prddes,id,wid)

    return render(request, 'wishlist.html', {'list': list,'wish_id':wish_id,'wid':wid,'s':s})


def cartdelete(request, id):
    a = cart.objects.get(id=id)
    a.delete()
    return redirect(cartdisplay)


def wishdelete(request, id):
    a = wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)


def cartbuy(request, id):
    a = cart.objects.get(id=id)
    im = str(a.upfile).split('/')[-1]
    if request.method == 'POST':
        name = request.POST.get('upname')
        description = request.POST.get('updiscription')
        quantity = request.POST.get('quantity')
        price = request.POST.get("upprice")
        b = buy(upname=name, updiscription=description, quantity=quantity, upprice=price)
        b.save()
        total = int(price) * int(quantity)
        return render(request, 'final.html',
                      {'total': total, 'name': name, 'description': description, 'quantity': quantity, 'price': price})
    return render(request, 'buyed.html', {'a': a, 'im': im})


def payment(request):
    if request.method == 'POST':
        sd=request.session['id']
        cardname = request.POST.get('cardname')
        cardnumber = request.POST.get('cardnumber')
        cardexpiration = request.POST.get("cardexpiration")
        securitycode= request.POST.get('securitycode')
        b=cardpayment(cardname=cardname,cardnumber=cardnumber,cardexpiration=cardexpiration,securitycode=securitycode)
        b.save()

        date=datetime.today().date()+timedelta(days=10)
        a=User.objects.get(id=sd)
        mail=a.email
        send_mail_register(mail,date)

        return render(request,'ordersuccess.html',{'date':date})
    return render(request, 'payment.html')


def send_mail_register(email,date):  # subject ,from email, recipient
    subject = "Order Summary"
    # f is astring literal which contains expressions inside curly brackets the expressions are replaced by values
    message = f' Congratulations Estimated Date of Delivery is {date}'
    email_from = EMAIL_HOST_USER  # from
    recipient = [email]  # to
    send_mail(subject, message, email_from, recipient)

def shopnotificationn(request):
    a = shopnotification.objects.all()
    notif=[]
    tim=[]
    for i in a:
        no=i.content
        notif.append(no)
        tm=i.date
        tim.append(tm)
    mylist=zip(notif,tim)
    return render(request,'shopnotification.html',{'mylist':mylist})

def usernotificationn(request):
    a = usernotification.objects.all()
    notif=[]
    time=[]
    for i in a:
        no=i.content
        notif.append(no)
        t=i.date
        time.append(t)
    mylist=zip(notif,time)
    return render(request,'usernotification.html',{'mylist':mylist})


