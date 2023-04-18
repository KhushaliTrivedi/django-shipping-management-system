from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('package', views.package, name='package'),
    path('package-details/<int:id>', views.packageDetails, name='package-details'),
    path('updateStatus/<int:id>', views.updateStatus, name='updateStatus'),
    path('profile', views.profile, name='profile'),
    path('updateProfile/<int:id>', views.updateProfile, name='updateProfile'),
]