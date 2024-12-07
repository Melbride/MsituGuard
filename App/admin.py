from django.contrib import admin
from .models import Profile, Alert, Resource, EmergencyContact, ResourceRequest, ForumPost, Comment # CustomUser
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User


# Action to approve selected alerts

@admin.action(description='Approve selected alerts')
def approve_alerts(modeladmin, request, queryset):
    queryset.update(is_approved=True)

# Admin class for Alert with the custom action

class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_active', 'is_approved')  
    actions = [approve_alerts]  # Register the approve_alerts action


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('Resource_Name', 'description', 'user', 'location', 'available', 'phoneNumber')



@admin.action(description='Approve selected resources')
def approve_resources(modeladmin, request, queryset):
    queryset.update(is_approved=True)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('Resource_Name', 'user',  'is_approved')  # Fields displayed in admin list view
    actions = [approve_resources]  # Register the approve_alerts action


# admin.site.register(Resource, ResourceAdmin)
class ResourceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'Resource_type', 'description', 'location', 'phoneNumber') 



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['bio', 'location', 'email', 'phoneNumber', 'profile_picture', 'first_name', 'last_name']


class UserAdmin(DefaultUserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location', 'get_phone_number')
    
    # Custom methods to display profile information in the user list
    def get_location(self, obj):
        return obj.profile.location
    get_location.short_description = 'Location'  # Column title

    def get_phone_number(self, obj):
        return obj.profile.phoneNumber
    get_phone_number.short_description = 'PhoneNumber'  # Column title

# Unregister the default User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)





admin.site.register(Alert, AlertAdmin)  # Register Alert with the AlertAdmin class
admin.site.register(Profile)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(EmergencyContact)
admin.site.register(ResourceRequest, ResourceRequestAdmin)
admin.site.register(ForumPost)
admin.site.register(Comment)
