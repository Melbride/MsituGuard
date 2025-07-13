from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('community', 'Community Member'),
        ('donor', 'Donor/Supporter'),
    ]
    
    DONOR_TIERS = [
        ('basic', 'Basic Supporter'),
        ('standard', 'Standard Donor'),
        ('premium', 'Premium Supporter'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(
        max_length=50,
        default=' ',
        validators=[RegexValidator(regex=r'^\d*$', message='Only numeric values are allowed')]
    )
    location = models.CharField(max_length=100, blank=True, default=' ')
    bio = models.TextField(default='Bio information not provided')
    email = models.EmailField(default='example@example.com')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    is_verified = models.BooleanField(default=False)
    verification_requested = models.BooleanField(default=False)
    
    # New fields for monetization
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES, default='community')
    donor_tier = models.CharField(max_length=50, choices=DONOR_TIERS, blank=True, null=True)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    donor_since = models.DateTimeField(blank=True, null=True)
    
    @property
    def is_donor(self):
        return self.account_type == 'donor'
    
    @property
    def donor_badge(self):
        # Only show badge if they've actually contributed money
        if not self.is_donor or self.total_donated <= 0:
            return None
        badges = {
            'basic': '🥉 Basic Supporter',
            'standard': '🥈 Community Donor', 
            'premium': '🥇 Premium Supporter'
        }
        return badges.get(self.donor_tier, '💝 Supporter')
    
    @property
    def is_active_donor(self):
        """Check if user is a donor who has actually contributed"""
        return self.is_donor and self.total_donated > 0




    def __str__(self):
        return self.user.username 

    

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    title = models.CharField(max_length=250)
    EMERGENCY_CHOICES = [
        ('fire', 'Fire'),
        ('flood', 'Flood'),
        ('earthquake', 'Earthquake'),
        ('medical', 'Medical'),
        ('other', 'Other'),
    ]
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_CHOICES, default='other')
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=50, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    phoneNumber = models.CharField(
        default = ' ',
        max_length=50,
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )

    def __str__(self):
        return self.title 

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('Food', 'Food'),
        ('Water', 'Water'),
        ('Clothes', 'Clothes'),
        ('Shelter', 'Shelter'),
        ('Medical', 'Medical'),
        ('Transportation', 'Transportation'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.resource_type
    

class EmergencyContact(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=50)
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

    HELP_TYPES = [
        ('Food', 'Food'),
        ('Water', 'Water'),
        ('Clothes', 'Clothes'),
        ('Shelter', 'Shelter'),
        ('Medical', 'Medical'),
        ('Transportation', 'Transportation'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    help_type = models.CharField(max_length=100, choices=HELP_TYPES)
    description = models.TextField()
    quantity_requested = models.PositiveIntegerField(default=1)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    matched_contribution = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.SET_NULL)
    response_message = models.TextField(blank=True, null=True)
    is_fulfilled = models.BooleanField(default=False)

    phoneNumber = models.CharField(
        max_length=50,
        default='',
        validators=[RegexValidator(regex=r'^\d+$', message='Only numeric values are allowed')]
    )

    location = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"User: {self.user.username}, Help Type: {self.help_type}"
    

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
