from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from adminDB.models import User
from adminDB.decorators import unauthenticated_user
from django.contrib import messages

@unauthenticated_user
@login_required(login_url='login')
def index(request):
    return redirect("/login")

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            data = User.objects.get(email=username)
            if data.is_admin == True:
                login(request,user)
                return HttpResponseRedirect('/admin')
            else:
                login(request,user)
                return HttpResponseRedirect('/team')
        else:
            messages.error(request, 'Please Enter Correct Username or Password!')
            return redirect('/login')
    return render (request,'login.html')
    
def LogoutPage(request):
    logout(request)
    return HttpResponseRedirect('/login')