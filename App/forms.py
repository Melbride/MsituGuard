from django import forms
from django.contrib.auth.models import User
from .models import Profile, Resource, Alert, ResourceRequest, ForumPost, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from .models import CustomUser
from django.core.validators import RegexValidator
# from .models import CustomUser
from captcha.fields import CaptchaField


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}))
    phoneNumber = forms.CharField(
        max_length=17,
        required=True,
        validators=[RegexValidator(regex=r'^\d*$', message='Only numeric values are allowed')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'})
    )        
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your neighborhood/area'}))
    bio = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Bio (optional)"
    )
    
    # New fields for account type
    account_type = forms.ChoiceField(
        choices=Profile.ACCOUNT_TYPES,
        widget=forms.RadioSelect,
        initial='community',
        label='Account Type'
    )
    
    donor_tier = forms.ChoiceField(
        choices=[('', 'Select donation level')] + Profile.DONOR_TIERS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Donation Level (for Donors)'
    )
    
    captcha = CaptchaField()
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)



    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create a strong password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("passwords do not match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.location = self.cleaned_data['location']

        if commit:
            user.save()

            # Always update or create profile data
            from django.utils import timezone
            profile_data = {
                'phoneNumber': self.cleaned_data['phoneNumber'],
                'location': self.cleaned_data['location'],
                'email': self.cleaned_data['email'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'bio': self.cleaned_data.get('bio', ''),
                'account_type': self.cleaned_data['account_type'],
            }
            
            # Add donor-specific fields if donor account
            if self.cleaned_data['account_type'] == 'donor' and self.cleaned_data.get('donor_tier'):
                profile_data['donor_tier'] = self.cleaned_data['donor_tier']
                profile_data['donor_since'] = timezone.now()
                # Set monthly contribution based on tier
                tier_amounts = {
                    'basic': 5.00,
                    'standard': 10.00,
                    'premium': 25.00
                }
                profile_data['monthly_contribution'] = tier_amounts.get(self.cleaned_data['donor_tier'], 0.00)
            
            Profile.objects.update_or_create(
                user=user,
                defaults=profile_data
            )

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )



class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resource_type', 'quantity', 'description', 'available', 'phoneNumber', 'location']

        
class AlertForm(forms.ModelForm):
    emergency_type = forms.ChoiceField(
        choices=[('', 'Select emergency type')] + Alert.EMERGENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Emergency Type"
    )
    
    class Meta:
        model = Alert
        fields = ['emergency_type', 'title', 'description', 'location', 'phoneNumber']
        labels = {
            'title': 'Emergency Summary',
            'description': 'Full Description',
            'location': 'Location',
            'phoneNumber': 'Phone Number',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary (e.g., "House fire on Main Street")'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Provide complete details: What happened? How many people affected? What help is needed? Any injuries?'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exact address or location'
            }),
            'phoneNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your contact number'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'profile'):
            self.fields['phoneNumber'].initial = user.profile.phoneNumber
        
    def save(self, commit=True):
        alert = super().save(commit=False)
        alert.is_active = True  # Always set to active for new alerts
        alert.visibility = 'public'  # Always public since admin approves
        if commit:
            alert.save()
        return alert


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phoneNumber', 'location', 'email', 'bio', 'profile_picture']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SuperuserProfileForm(ProfileForm):
    pass


class ResourceRequestForm(forms.ModelForm):
    help_type = forms.ChoiceField(choices=ResourceRequest.HELP_TYPES, label="Help Type")

    class Meta:
        model = ResourceRequest
        fields = ['help_type', 'description', 'phoneNumber', 'location']
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Briefly describe your situation or what kind of assistance would help.',
                'rows': 4,
            }),
            'phoneNumber': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter your location'}),
        }


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

   
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']

class FormComment(forms.ModelForm):
    class  Meta:
        model = Comment
        fields = ('content',)

        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),

        }

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phoneNumber = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'phoneNumber', 'location')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conform new password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


# class LoginFormWithCaptcha(AuthenticationForm):
#     captcha = CaptchaField(widget=CaptchaV2Checkbox)


