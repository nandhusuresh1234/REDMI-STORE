from django.urls import path
from .views import *


urlpatterns=[
    path('shopregister/',shopregisterr),
    path('shoplogin/',shoplogin1),
    path('upload/',upload),
    path('profile/',profile1),
    path('productdisplay/',productdisplay),
    path('delete/<int:id>',delete),
    path('edit/<int:id>',edit),
    path('success/',success),
    path('userprofile/',userprofile),
    path('userregistration/',userregistration),
    path('verify/<auth_token>',verify),
    path('userlogin/',login),
    path('index/',index),
    path('userdisplay/',userproductdisplay),
    path('cart/<int:id>/',addtocart),
    path('wishlist/<int:id>/',addtowishlist),
    path('wishlistdisplay/',wishlistdisplay),
    path('cartdisplay/',cartdisplay),
    path('cartdelete/<int:id>',cartdelete),
    path('wishdelete/<int:id>',wishdelete),
    path('cartbuy/<int:id>',cartbuy),
    path('payment/',payment),
    path('viewallp/',viewallp),
    path('addtocart1/<int:id>',addtocart1),
    path('shopnotification/',shopnotificationn),
    path('usernotification/',usernotificationn),
    ]