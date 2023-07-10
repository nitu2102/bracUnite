from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#For activating the account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError


#Getting tokens from utils.py
from .utils import TokenGenerator, generate_token


#Email import
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage


#threading
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()



def dashboard(request):
    return render(request, 'dashboard.html')
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def portfolio(request):
    return render(request, 'portfolio.html')
def study(request):
    return render(request, 'study.html')
def contact(request):
    return render(request, 'contact.html')
def student(request):
    return render(request, 'student.html')
def alumni(request):
    return render(request, 'alumni.html')
def faculty(request):
    return render(request, 'faculty.html')

def Handle_login(request):
    storage = messages.get_messages(request)
    storage.used = True   #clear error msg

    if request.method=="POST":
        username = request.POST['email']
        userpassword = request.POST['password1']

        myuser = authenticate(username=username, password=userpassword) #username and password match test

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Logged in successfully")
            return render(request, "dashboard.html")
        else:
            messages.error(request, "Something went wrong!")
            return redirect("/login")
    
    return render(request, "login.html")


def Handle_signup(request):
    #to clear multiple error message
    storage = messages.get_messages(request)
    storage.used = True

    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password!=confirm_password:
            messages.warning(request, "Password is not matching!")
            return render(request, 'signup.html')

        try:
            if User.objects.get(username=email): #i have used email as username
                messages.warning(request, "Email is taken!")
                return render(request, 'signup.html')

        except Exception as identifier:
            pass

        #username email and password
        user = User.objects.create_user(email, email, password) #username=email,email,password
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)), #pk=primary key
            'token': generate_token.make_token(user)
        })

        email_message = EmailMessage(email_subject, message,settings.EMAIL_HOST_USER, [email],) #email sender
        EmailThread(email_message).start() #fast email sender
        messages.info(request, "Activate your account by clicking link on your email")
        return redirect('/login')


        messages.info(request, "SignUp Successful! Please Login")
        return redirect('/login')

    return render(request, 'signup.html')



def Handle_logout(request):
    storage = messages.get_messages(request)
    storage.used = True

    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully!")
            return redirect('/login')
        return render(request, 'activatefail.html')


