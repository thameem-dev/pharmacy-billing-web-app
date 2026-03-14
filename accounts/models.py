from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('system_admin', 'System Admin'),
        ('manager', 'Manager'),
        ('biller', 'Biller'),
        ('inventory', 'Inventory'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES,)


class LoginHistory(models.Model):
    LOG_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=10, choices=LOG_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.log_type} at {self.date}"