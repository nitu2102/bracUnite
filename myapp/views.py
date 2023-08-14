from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from .models import Profile
from .forms import ProfileUpdateForm
from django.shortcuts import render, get_object_or_404



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


@login_required(login_url='/login')
def dashboard(request):
    CurrentUser = request.user
    return render(request, 'dashboard.html', {'CurrentUser':CurrentUser})

def home(request):
    if request.user.is_authenticated:
        CurrentUser = request.user
    return render(request, 'dashboard.html', {'CurrentUser':CurrentUser})
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')




@login_required(login_url='/login')
def portfolio(request, user_id):
    userProfile = Profile.objects.get(id=user_id)

    print(type(userProfile.research_interest))
    return render(request, 'portfolio.html', {'userProfile':userProfile})





def study(request):
    return render(request, 'study.html')
def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='/login')
def student(request):
    students = Profile.objects.filter(is_active=True)
    return render(request, 'student.html', {'students':students})

@login_required(login_url='/login')
def alumni(request):
    alumnis = Profile.objects.filter(is_active=True)
    return render(request, 'alumni.html', {'alumnis':alumnis})

@login_required(login_url='/login')
def faculty(request):
    faculties = Profile.objects.filter(is_active=True)
    return render(request, 'faculty.html', {'faculties':faculties})

def Handle_login(request):
    storage = messages.get_messages(request)
    storage.used = True   #clear error msg

    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method=="POST":
        username = request.POST['email']
        userpassword = request.POST['password1']

        myuser = authenticate(username=username, password=userpassword) #username and password match test

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Logged in successfully")
            return redirect("/dashboard")
        else:
            messages.error(request, "Something went wrong!")
            return redirect("/login")
    
    return render(request, "login.html")


def Handle_signup(request):
    #to clear multiple error message
    storage = messages.get_messages(request)
    storage.used = True

    if request.method=="POST":
        print(request.POST["signupType"])
        userRole = request.POST["signupType"]
        profileName = request.POST['username']
        studentId = ""
        if request.POST["studentID"] is not None:
            studentId = request.POST["studentID"]
        
            


        email = request.POST['email']
        if not email.endswith("g.bracu.ac.bd"):
            if userRole!="Faculty":
                messages.warning(request, "You must insert a valid gsuite email!")
                return render(request, 'signup.html')
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
        
        user.profile.name = profileName
        user.profile.role = userRole
        user.profile.student_id = studentId
        print(user.profile.name, user.profile.role)
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def profile_update(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Dashboard')  # Redirect to the profile detail page after successful update
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile_update.html', {'form': form})
