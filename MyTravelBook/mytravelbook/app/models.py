from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    username = None
    groups = None
    user_permissions = None
    
    
    name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    
    
    class Meta:
        db_table = "users"
    # Create your models here.
