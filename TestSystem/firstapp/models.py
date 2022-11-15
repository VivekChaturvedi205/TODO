from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, email_verified, password=None,):
        if not email:
            raise ValueError("Email Required!!!")
        user = self.model(
            email=self.normalize_email(email),
            email_verified=email_verified
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, email_verified, password=None):
        user = self.create_user(
            email, 
            email_verified=email_verified,
            password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    Token=models.CharField(max_length=150)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email_verified']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class todolist(models.Model):
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    details=models.TextField()
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email+self.title