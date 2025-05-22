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
    is_verified = models.BooleanField(default=False)
    verification_requested = models.BooleanField(default=False)

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
    RESOURCE_TYPES = [
    ('Food', 'Food'),
    ('Clothes', 'Clothes'),
    ('Shelter', 'Shelter'),
    ('Medical', 'Medical'),
]
    # Resource_Name = models.CharField(max_length=250)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)  # Who contributed
    resource_type = models.CharField(max_length=100, choices=RESOURCE_TYPES)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    phoneNumber = models.CharField(
        max_length=17,
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )
    location = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    date_contributed = models.DateTimeField(auto_now_add=True)
    is_allocated = models.BooleanField(default=False)  # Optional: if resource is already allocated
    available = models.BooleanField(default=True)
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.resource_type
    

class EmergencyContact(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    email = models.EmailField(default='contact@example.com')
    organization = models.CharField(max_length=250)


    def __str__(self):
        return f"{self.name} ({self.organization})"

class ResourceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
    ]

    RESOURCE_TYPES = [
        ('Food', 'Food'),
        ('Clothes', 'Clothes'),
        ('Shelter', 'Shelter'),
        ('Medical Aid', 'Medical Aid'),
        ('Water', 'Water'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=100, choices=RESOURCE_TYPES)
    description = models.TextField()
    quantity_requested = models.PositiveIntegerField(default=1)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    matched_contribution = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.SET_NULL)
    response_message = models.TextField(blank=True, null=True)
    is_fulfilled = models.BooleanField(default=False)

    phoneNumber = models.CharField(
        max_length=17,
        default='',
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )

    location = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"User: {self.user.username}, Resource Type: {self.resource_type}"
    

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
    # name = models.CharField(max_length=250,  default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"   
