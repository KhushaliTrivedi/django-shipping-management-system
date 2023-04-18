from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from datetime import date

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_time = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    

# Route Model
class Route(models.Model):
    start = models.TextField()
    end = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True, blank=True)


# Vehicle Model
class Vehicle(models.Model):
    AVAILABILITY = (
        (0, 'Available'),
        (1, 'In Use'),
        (2, 'Repair'),
    )
    model = models.TextField()
    vehicle_number = models.TextField()
    is_available = models.IntegerField(choices=AVAILABILITY, default=0)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)


# Package Model
class Package(models.Model):
    STATUS = (
        (0, 'Not Delivered'),
        (1, 'Delivered'),
        (2, 'Processing'),
    )

    title = models.TextField()
    sender = models.TextField()
    receiver = models.TextField()
    description = models.TextField()
    is_delivered = models.IntegerField(choices=STATUS, default=0)
    delivery_due = models.DateField()
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    route = models.ForeignKey(Route, default=2, null=False,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, default=2,null=False, on_delete=models.CASCADE)
    team = models.TextField()
    
    def team_list(self):
        data = list(map(int, self.team.split(",")))
        users = []
        for d in data:
            try:
                u = User.objects.get(id=d)
            except User.DoesNotExist:
                continue
            users.append(u)
            return users
    
    def due_days(self):
        data = self.delivery_due
        today = date.today()
        d3 = [(data - today).days]
        return d3
