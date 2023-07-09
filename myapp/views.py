from django.shortcuts import render
from django.http import HttpResponse, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#Add another import here

#Email import
# from django.core.mail import send_mail
# from django.conf import settings
# from django.core import mail
# from django.core.mail.message import EmailMessage

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

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password!=confirm_password:
            messages.warning(request, "Password is not matching!")
            return render(request, 'signup.html')

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is taken!")
                return render(request, 'signup.html')

        except Exception as identifier:
            pass

        myuser = User.objects.create_user(email, email, password)
        myuser.save()
        messages.info(request, "SignUp Successful! Please Login")
        return redirect('/login')

    return render(request, 'signup.html')



    return render(request, 'signup.html')


