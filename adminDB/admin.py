from django.contrib import admin
from .models import User, Route, Vehicle, Package
# Register your models here.

admin.site.register(User)
admin.site.register(Route)
admin.site.register(Vehicle)
admin.site.register(Package)