from django import forms

class shopNregif(forms.Form):
    uname = forms.CharField(max_length=30)
    uaddress = forms.CharField(max_length=30)
    ushopid = forms.IntegerField()
    uemail = forms.EmailField()
    uphone = forms.IntegerField()
    upassword = forms.CharField(max_length=20)
    upassword2=forms.CharField(max_length=20)


class shoploginF(forms.Form):
    uname=forms.CharField(max_length=30)
    upassword=forms.CharField(max_length=20)

class uploadform(forms.Form):
    upname = forms.CharField(max_length=30)
    upprice = forms.IntegerField()
    updiscription = forms.CharField(max_length=30)
    upfile = forms.FileField()

    class cardpayment(forms.Form):
        cardname = forms.CharField(max_length=30)
        cardnumber = forms.IntegerField()
        cardexpiration = forms.CharField(max_length=30)
        securitycode = forms.CharField(max_length=30)
