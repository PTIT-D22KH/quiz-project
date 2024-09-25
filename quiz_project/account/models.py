from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email_adress = models.EmailField(max_length=254, null=True, unique=True)
    bio = models.TextField(null=True)
    profile_img = models.ImageField(upload_to='static\images',null=True,default='static\images\R.png')
    location = models.CharField(max_length=30, null=True)
    GENDER=(
        ('Nam','Nam'),
        ('Nu', 'Nu'),
        ('Khac', 'Khac'),
    )
    gender = models.CharField(max_length=10, null=True,choices=GENDER)