from django.shortcuts import render, redirect
from .models import User, Route, Vehicle, Package
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from .decorators import allowed_users
from itertools import chain
# Create your views here.


# Render Index Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def index(request):
    last_accounts = User.objects.order_by('-date_time')[:3]
    last_packages = Package.objects.order_by('-date_time')[:3]
    last_rows = list(chain(last_accounts, last_packages))
    last_rows.sort(key=lambda r: r.date_time, reverse=True)
    package = Package.objects.all()
    route = Route.objects.all()
    vehicle = Vehicle.objects.all()
    user = User.objects.all()
    return render(request, 'index.html', {
        'last_rows': last_rows,
        'packageC': package.count(),
        'routeC': route.count(),
        'vehicleC': vehicle.count(),
        'userC': user.count(),
    })


# Render Profile Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profile(request, id=None):
    if id:
        data = User.objects.get(id=id)
        context = {
            'data': data,
            'id': id
        }
    else:
        data = User.objects.all()
        context = {
            'data': data,
        }

    return render(request, 'profile.html', context)


# Create an Account and store the data in Database
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProfile(request):

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # Check if Existing User
        users = User.objects.all()
        for n in users:
            if n.email == username:
                messages.error(request, 'User with this Email Exists!')
                return redirect('/admin/profile')

        if role == 'admin':
            is_admin = True
        else:
            is_admin = False

        Data = User(
            name=name,
            email=username,
            is_admin=is_admin,
        )
        Data.set_password(password)
        Data.save()
        messages.success(request, 'Account Registered Successfully!')
    return redirect('/admin/profile')


# Delete an Account and remove all data from the Database
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProfile(request, id):

    deleteUser = User.objects.get(id=id)
    deleteUser.delete()
    messages.success(request, 'Account Deleted Successfully!')

    return redirect('/admin/profile')


# Update an Account
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateRecord(request, id):
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    role = request.POST['role']

    if role == 'admin':
        is_admin = True
    else:
        is_admin = False

    user = User.objects.get(id=id)
    user.name = name
    user.email = username
    user.is_admin = is_admin

    if password:
        user.set_password(password)
    user.save()

    messages.success(request, 'Account details Updated Successfully!')
    return redirect('/admin/profile')


# Render Route Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def route(request, id=None):
    if id:
        data = Route.objects.get(id=id)
        context = {
            'data': data,
            'id': id
        }
    else:
        data = Route.objects.all()
        context = {
            'data': data
        }
    return render(request, 'route.html', context)


# Create a Route
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addRoute(request):

    if request.method == 'POST':
        start = request.POST['startPoint']
        end = request.POST['endPoint']

        # Check if Existing User
        existingRoutes = Route.objects.all()
        for val in existingRoutes:
            if ((val.start.lower() == start.lower()) and (val.end.lower() == end.lower())):
                messages.error(request, 'The Route you have entered Exists!')
                return redirect('/admin/route')

        Data = Route(
            start=start,
            end=end,
            date_time=datetime.datetime.now(),
        )
        Data.save()
        messages.success(request, 'Route Created Successfully!')
    return redirect('/admin/route')


# Delete a Route
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteRoute(request, id):

    deleteRoute = Route.objects.get(id=id)
    deleteRoute.delete()
    messages.success(request, 'Route Deleted Successfully!')

    return redirect('/admin/route')


# Update a Route
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateRoute(request, id):
    start = request.POST['startPoint']
    end = request.POST['endPoint']

    route = Route.objects.get(id=id)
    route.start = start
    route.end = end
    route.save()

    messages.success(request, 'Route details Updated Successfully!')
    return redirect('/admin/route')


# Render Vehicle Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def vehicle(request, id=None):
    if id:
        data = Vehicle.objects.get(id=id)
        context = {
            'data': data,
            'id': id
        }
    else:
        data = Vehicle.objects.all()
        context = {
            'data': data
        }
    return render(request, 'vehicle.html', context)


# Add Vehicle
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addVehicle(request):

    if request.method == 'POST':
        vNumber = request.POST['vNumber']
        vModel = request.POST['vModel']
        availability = request.POST['availability']

        # Check if Vehicle Exist
        existingVehicles = Vehicle.objects.all()
        for val in existingVehicles:
            if (val.vehicle_number.lower() == vNumber.lower()):
                messages.error(request, 'The Vehicle you have entered Exists!')
                return redirect('/admin/vehicle')

        Data = Vehicle(
            vehicle_number=vNumber,
            model=vModel,
            is_available=availability,
            date_time=datetime.datetime.now(),
        )
        Data.save()
        messages.success(request, 'Vehicle Added Successfully!')
    return redirect('/admin/vehicle')


# Delete Vehicle
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteVehicle(request, id):

    deleteV = Vehicle.objects.get(id=id)
    deleteV.delete()
    messages.success(request, 'Vehicle Deleted Successfully!')

    return redirect('/admin/vehicle')


# Update Vehicle
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateVehicle(request, id):

    if request.method == 'POST':
        vNumber = request.POST['vNumber']
        vModel = request.POST['vModel']
        availability = request.POST['availability']

        vehicle = Vehicle.objects.get(id=id)
        vehicle.vehicle_number = vNumber
        vehicle.model = vModel
        vehicle.is_available = availability
        vehicle.save()

        messages.success(request, 'Vehicle details Updated Successfully!')
        return redirect('/admin/vehicle')


# Render Package Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def package(request, id=None):
    if id:
        package = Package.objects.get(id=id)
        context = {
            'package': package,
            'id': id,
        }
    else:
        package = Package.objects.all()
        route = Route.objects.all()
        vehicle = Vehicle.objects.all()
        team = User.objects.all()
        context = {
            'package': package,
            'route': route,
            'vehicle': vehicle,
            'team': team
        }
    return render(request, 'package.html', context)


# Add Package
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addPackage(request):

    if request.method == 'POST':
        title = request.POST['pTitle']
        sender = request.POST['sName']
        receiver = request.POST['rName']
        description = request.POST['description']
        delivery_date = request.POST['dueDate']
        route = request.POST['route']
        vehicle = request.POST['vehicle']
        team = request.POST['team']

        Data = Package(
            title=title,
            sender=sender,
            receiver=receiver,
            description=description,
            delivery_due=delivery_date,
            route_id=route,
            vehicle_id=vehicle,
            team=team,
            date_time=datetime.datetime.now(),
        )
        Data.save()

        v = Vehicle.objects.get(id=vehicle)
        v.is_available = 1
        v.save()

        messages.success(request, 'Package Added Successfully!')
        return redirect('/admin/package')


# Delete Package
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deletePackage(request, id):

    deleteP = Package.objects.get(id=id)
    deleteP.delete()
    messages.success(request, 'Package Deleted Successfully!')

    return redirect('/admin/package')


# Update Package
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePackage(request, id):

    if request.method == 'POST':
        title = request.POST['pTitle']
        sender = request.POST['sName']
        receiver = request.POST['rName']
        description = request.POST['description']
        delivery_date = request.POST['dueDate']
        status = request.POST['status']

        pack = Package.objects.get(id=id)
        pack.title = title
        pack.sender = sender
        pack.receiver = receiver
        pack.description = description
        pack.delivery_due = delivery_date
        pack.is_delivered = status
        pack.save()

        messages.success(request, 'Package details Updated Successfully!')
        return redirect('/admin/package')
