from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return render(request, 'home.html')
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
    return render(request, 'signup.html')

