from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User, Package

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            email = request.user
            userData = User.objects.get(email=email)
            if userData.is_admin == True:
                return redirect('/admin')
            else:
                return redirect('/team')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            email = request.user
            userData = User.objects.get(email=email)
            if userData.is_admin == True:
                role = 'admin'
            else:
                role = 'team'
            
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You have no Permission to View this page")
        return wrapper_func
    return decorator
