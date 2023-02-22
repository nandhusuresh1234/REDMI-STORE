from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class shopregister(models.Model):

    uname = models.CharField(max_length=30)
    uaddress = models.CharField(max_length=30)
    ushopid = models.IntegerField()
    uemail = models.EmailField()
    uphone = models.IntegerField()
    upassword = models.CharField(max_length=20)
    upassword2 = models.CharField(max_length=20)

    def __str__(self):
        return self.uname,self.uaddress,self.uemail,self.uphone


class uploadmodel(models.Model):
    shopid=models.IntegerField()
    upname=models.CharField(max_length=30)
    upprice=models.IntegerField()
    updiscription=models.CharField(max_length=30)
    upfile=models.ImageField(upload_to='rc/static')

    def __str__(self):
        return self.upname

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    userid=models.IntegerField()
    upname=models.CharField(max_length=30)
    upprice=models.IntegerField()
    updiscription=models.CharField(max_length=30)
    upfile=models.ImageField()

    def __str__(self):
        return self.upname

class wishlist(models.Model):
    userid=models.IntegerField()
    upname=models.CharField(max_length=30)
    upprice=models.IntegerField()
    updiscription=models.CharField(max_length=30)
    upfile=models.ImageField()

    def __str__(self):
        return self.upname

class buy(models.Model):
    upname=models.CharField(max_length=30)
    upprice=models.IntegerField()
    updiscription=models.CharField(max_length=30)
    upfile=models.ImageField()
    quantity=models.IntegerField()

    def __str__(self):
        return self.upname,self.updiscription,self.quantity

class cardpayment(models.Model):
    cardname=models.CharField(max_length=30)
    cardnumber=models.IntegerField()
    cardexpiration=models.CharField(max_length=30)
    securitycode=models.CharField(max_length=30)

    def __str__(self):
        return self.cardexpiration,self.securitycode,self.cardnumber


class shopnotification(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)

class usernotification(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)