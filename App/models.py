from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(
        max_length=17,
        default=' ',
        validators=[RegexValidator(regex=r'^\d*$', message='Only numeric values are allowed')]
    )
    location = models.CharField(max_length=200, default='')
    bio = models.TextField(default='Bio information not provided')
    email = models.EmailField(default='example@example.com')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    # last_namee = models.CharField(max_length=100, default='')


    def __str__(self):
        return self.user.username 

    


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')


    def __str__(self):
        return self.title 


class Resource(models.Model):
    Resource_Name = models.CharField(max_length=250)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)  
    available = models.BooleanField(default=True)
    phoneNumber = models.CharField(
        max_length=17,
        default=' ',
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, default='')  # Location of donor


    def __str__(self):
        return self.Resource_Name
    

class EmergencyContact(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    email = models.EmailField(default='contact@example.com')
    organization = models.CharField(max_length=250)


    def __str__(self):
        return f"{self.name} ({self.organization})"

class ResourceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)  # Add this field
    Resource_type = models.CharField(max_length=100, default='')
    description = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    # is_approved = models.BooleanField(default=False)  # New field to track approval status
    is_fulfilled = models.BooleanField(default=False)
    phoneNumber = models.CharField(
        max_length=17,
        default=' ',
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, default='')  # Location of donor
    # resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)  # Make sure this field exists



    def __str__(self):
        return f"User: {self.user.username}, Resource Type: {self.Resource_type}"
    

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250,  default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"   
