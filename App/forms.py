from django import forms
from django.contrib.auth.models import User
from .models import Profile, Resource, Alert, ResourceRequest, ForumPost, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from .models import CustomUser
from django.core.validators import RegexValidator



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phoneNumber = forms.CharField(
        max_length=17,
        required=True,  # Allow blank phone numbers
        validators=[RegexValidator(regex=r'^\d*$', message='Only numeric values are allowed')]  # Change to r'^\d*$' to allow empty
    )        
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'email',  'phoneNumber',  'first_name', 'last_name' ,'location',]


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("passwords do not match")
        return cleaned_data
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         # Create the profile instance linked to the user
    #         Profile.objects.create(
    #             user=user,
    #             phoneNumber=self.cleaned_data['phoneNumber'],
    #             location=self.cleaned_data['location']
    #         )
    #     return user


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
        fields = ['name', 'description', 'available', 'phoneNumber', 'location']

        


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['title', 'description', 'location', 'is_active', 'visibility']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'email', 'phoneNumber']
        
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(  # Use TextInput for phone number
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your phone number'  # Optional placeholder
                }
            )
        }
    def clean_phoneNumber(self):
        phone_number = self.cleaned_data.get('phoneNumber')
        if not phone_number.isdigit():
            raise forms.ValidationError("Only numeric values are allowed.")
        return phone_number




class SuperuserProfileForm(ProfileForm):
    pass


class ResourceRequestForm(forms.ModelForm):
    class Meta:
        model = ResourceRequest
        fields = ['Resource_type', 'description', 'phoneNumber', 'location']


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

   
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FormComment(forms.ModelForm):
    class  Meta:
        model = Comment
        fields = ('name',  'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
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
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'phone_number', 'location')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conform new password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

