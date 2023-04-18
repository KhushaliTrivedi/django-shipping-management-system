from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('addProfile', views.addProfile, name='addProfile'),
    path('profile/updateProfile/<int:id>', views.profile, name='profile'),
    path('updateRecord/<int:id>', views.updateRecord, name='updateRecord'),
    path('profile/deleteProfile/<int:id>', views.deleteProfile, name='deleteProfile'),

    # Routes
    path('route', views.route, name='route'),
    path('addRoute', views.addRoute, name='addRoute'),
    path('editRoute/<int:id>', views.route, name='route'),
    path('updateRoute/<int:id>', views.updateRoute, name='updateRoute'),
    path('deleteRoute/<int:id>', views.deleteRoute, name='deleteRoute'),

    # Vehicle
    path('vehicle', views.vehicle, name='vehicle'),
    path('addVehicle', views.addVehicle, name='addVehicle'),
    path('editVehicle/<int:id>', views.vehicle, name='vehicle'),
    path('updateVehicle/<int:id>', views.updateVehicle, name='updateVehicle'),
    path('deleteVehicle/<int:id>', views.deleteVehicle, name='deleteVehicle'),

    # Packages
    path('package', views.package, name='package'),
    path('addPackage', views.addPackage, name='addPackage'),
    path('editPackage/<int:id>', views.package, name='package'),
    path('updatePackage/<int:id>', views.updatePackage, name='updatePackage'),
    path('deletePackage/<int:id>', views.deletePackage, name='deletePackage'),

]