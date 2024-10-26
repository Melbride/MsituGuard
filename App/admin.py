from django.contrib import admin
from .models import Profile, Alert, Resource, EmergencyContact, ResourceRequest, ForumPost, Comment # CustomUser

# Action to approve selected alerts
@admin.action(description='Approve selected alerts')
def approve_alerts(modeladmin, request, queryset):
    queryset.update(is_approved=True)

# Admin class for Alert with the custom action
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_active', 'is_approved')  # Fields displayed in admin list view
    actions = [approve_alerts]  # Register the approve_alerts action

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'available')

# admin.site.register(Resource, ResourceAdmin)
class ResourceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'Resource_type', 'description', 'location', 'phoneNumber')  
    # list_filter = ('is_approved',)  # Add a filter to easily see approved/unapproved requests
    # actions = ['approve_requests']  # Custom action for bulk approval
    # # Custom action to approve requests
    # def approve_requests(self, request, queryset):
    #     queryset.update(is_approved=True)
    # approve_requests.short_description = "Approve selected resource requests"
# Register the models with the admin
admin.site.register(Alert, AlertAdmin)  # Register Alert with the AlertAdmin class
admin.site.register(Profile)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(EmergencyContact)
admin.site.register(ResourceRequest, ResourceRequestAdmin)
admin.site.register(ForumPost)
admin.site.register(Comment)
