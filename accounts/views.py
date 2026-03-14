from django.shortcuts import render,redirect
from django.contrib import messages
import re
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from .models import *

# This view handles the login process of the website
def loginPage(request):
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            LoginHistory.objects.create(user=user,log_type='login')
            login(request,user)
            return redirect('loginhistory')
        else:
            messages.error(request,"Login failed. Check your username and password.")
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request,'login.html')

@login_required
def addUser(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        role = request.POST.get('role')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            messages.error(request,"username already exist , try other name")
            return render(request,'add_user.html') 
        except Exception:
            new_user =User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,role=role)
            messages.success(request,"Account created successfully")
            return render(request,'add_user.html')
        
    return render(request,'add_user.html')

def passwordReset(request):
    return render(request,'login.html')



@login_required
def logoutPage(request):
    LoginHistory.objects.create(user=request.user,log_type='logout')
    logout(request)
    return redirect('login')

@login_required
def loginHistory(request):
   login_history =  LoginHistory.objects.all()
   return render(request,'login_history.html',{'history':login_history})