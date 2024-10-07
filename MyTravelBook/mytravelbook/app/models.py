from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です。")
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            **extra_fields)
        user.set_password(password)  # パスワードをハッシュ化
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password=None, **extra_fields):
        """スーパーユーザーを作成するメソッド"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("スーパーユーザーにはis_staff=Trueを設定する必要があります。")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("スーパーユーザーにはis_superuser=Trueを設定する必要があります。")

        return self.create_user(name, email, password, **extra_fields)

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
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        db_table = "users"
 
