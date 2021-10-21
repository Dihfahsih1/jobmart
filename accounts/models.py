from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={"required": "Role must be provided"})
    
    company_name = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.FileField(upload_to='media/resume/', null=True, blank=True, default="media/default/avatar.png")
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    resume = models.FileField(upload_to='media/resume/', null=True, blank=True)
    reg_document = models.FileField(upload_to='media/docs/', null=True, blank=True)
    registration_no = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    working_experience = models.IntegerField(default=0)
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()
    
     
    
#skills model    
class Skillset(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    skill = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)