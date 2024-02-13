"""
URL configuration for shoaibCommerece project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
 
from django.urls import path
from myinvestment.views import withdraw,pricing,profile,referal,plandetail,purchased_plan, contact  ,about,updteprofile,dashboard,history,check_email,check_username
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('updteprofile/',updteprofile,name='change_profile'),
    path('purchased_plan/',purchased_plan,name='payment'),
    path('plandetail/<str:id>',plandetail,name='plandetail'),
    path('withdraw/',withdraw,name='withdraw'),
     
    path('pricing/',pricing,name='pricing'),
    path('profile/',profile,name='profile'),
    path('referal/',referal,name='referal'),
    path('dashboard/',dashboard,name='dashboard'),
    path('history/',history,name='history'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
   
    path('check_username/',check_username,name='check_username'),
    path('check_email/',check_email,name='check_email'),
    path('login_old/', views.LoginView.as_view(template_name='login.html'), name='login_old'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("password_reset/", views.PasswordResetView.as_view(template_name='reset_password.html'), name="password_reset"),
    path(
        "password_reset_done/",
        views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name='password_set.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
        name="password_reset_complete",
    ),

    
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
