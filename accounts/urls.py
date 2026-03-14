from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('adduser/', views.addUser, name='adduser'),
    path('reset_password/', views.passwordReset, name='reset_password'),
    path('logout/', views.logoutPage, name='logout'),
    path('loginhistory/', views.loginHistory, name='loginhistory'),
]
