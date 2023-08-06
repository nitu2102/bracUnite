from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='HOME'),
    path('dashboard/', views.dashboard, name='Dashboard'),
    path('about/', views.about, name='ABOUT'),
    path('portfolio/', views.portfolio, name='PORTFOLIO'),
    path('study/', views.study, name='STUDY'),
    path('contact/', views.contact, name='CONTACT ME'),
    path('login/', views.Handle_login, name='Log In'),
    path('signup/', views.Handle_signup, name='Sign Up'),
    path('logout/', views.Handle_logout, name='Log Out'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('student/', views.student, name='Student'),
    path('alumni/', views.alumni, name='Alumni'),
    path('faculty/', views.faculty, name='Faculty'),
    path('edit/', views.profile_update, name='profile_update'),
]