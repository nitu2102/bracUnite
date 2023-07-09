from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('home/', views.home, name='HOME'),
    path('about', views.about, name='ABOUT'),
    path('portfolio/', views.portfolio, name='PORTFOLIO'),
    path('study/', views.study, name='STUDY'),
    path('contact/', views.contact, name='CONTACT ME'),
    path('login/', views.login, name='Log In'),
    path('signup/', views.signup, name='Sign Up'),
]