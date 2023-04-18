from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from adminDB.decorators import allowed_users
from adminDB.models import Package, Route, Vehicle, User
from django.contrib import messages

# Create your views here.

# Render Dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def index(request):
    logged_user = request.user.id
    delivered = Package.objects.filter(is_delivered=1,team__contains=logged_user)
    processing = Package.objects.filter(is_delivered__in=[0, 2],team__contains=logged_user)
    package = Package.objects.filter(team__contains=logged_user).order_by("-date_time")[:5]
    context = {
        'packageC': package.count(),
        'package': package,
        'delivered': delivered.count(),
        'processing': processing.count(),
    }
    return render(request, 'dashboard.html',context)


# Render Package Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def package(request):
    logged_user = request.user.id
    data = Package.objects.filter(team__contains=logged_user)
    context = {
        'data' : data,
    }
    return render(request, 'T-package.html', context)



# Render Package Details Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def packageDetails(request,id):
    data = Package.objects.get(id=id)
    route = Route.objects.all()
    vehicle = Vehicle.objects.all()
    team = User.objects.all()
    context = {
        'data' : data,
        'route': route,
        'vehicle': vehicle,
        'team': team
    }
    return render(request, 'package-details.html',context)


# Update Status 
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def updateStatus(request,id):
    if request.method == 'POST':
        status = request.POST['status']
        vehicleId = request.POST['vehicleId']
        print(status)
        if status == '1':
            v = Vehicle.objects.get(id=vehicleId)
            v.is_available = 0
            v.save()
            print(v)
        else:
            v = Vehicle.objects.get(id=vehicleId)
            v.is_available = 1
            v.save()
            print('else')


    data = Package.objects.get(id=id)
    data.is_delivered = status
    data.save()
    messages.success(request, 'Status Updated Successfully!')
    return redirect('/team/package')



# Render Profile Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'T-profile.html',context)


# Update Profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['team'])
def updateProfile(request,id):
    if id == request.user.id:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.get(id=id)
            user.name = name
            user.email = email

            if password:
                user.set_password(password)
            user.save()

    messages.success(request, 'Profile Updated Successfully!')
    return redirect('/team/profile')
    