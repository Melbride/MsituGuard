
from django.urls import path, include
from . import views
from .views import ussd_callback

from django.contrib.auth import views as auth_views
from .views import UseRegisterView
from .views import(HomeView,   UserLogoutView, ResourceListView, ResourceCreateView,
                   ResourceUpdateView, ResourceDeleteView, EmergencyContactListView, ProfileDetailView, 
                   ResourceDetailView, AlertListView, AlertCreateView, AlertUpdateView, AlertDetailView,
                   LatestAlertsView, ResourceRequestCreateView, ResourceRequestListView,
                   ForumPostListView, ForumPostCreateView, ForumPostDetailView,  AddCommentView, UserEditView, ApprovedAlertListView,
                   PasswordChangeView)
#,UserRegisterView
                   
urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('', include('django.contrib.auth.urls')), 
    path('register/', UseRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/new/', ResourceCreateView.as_view(), name='resource_create'),
    path('resource/edit/<int:pk>/', ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource_delete'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('contacts/', EmergencyContactListView.as_view(), name='contact_list'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    # path('profile/remove_picture/', remove_profile_picture, name='remove_profile_picture'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('alerts/', AlertListView.as_view(), name='alert_list'),
    path('alerts/new/', AlertCreateView.as_view(), name='alert_create'),  # Use alert_create
    path('alert/edit/<int:pk>/', AlertUpdateView.as_view(), name='alert_update'),
    path('latest-alerts/', LatestAlertsView.as_view(), name='latest_alerts'),
    path('alerts/<int:pk>/', AlertDetailView.as_view(), name='alert_detail'),
    path('approved-alerts/', ApprovedAlertListView.as_view(), name='approved_alerts'),
    path('request-resource/', ResourceRequestCreateView.as_view(), name='request_resource'),
    path('resource-requests/', ResourceRequestListView.as_view(), name='resource_requests'),
    # path('resources/', ApprovedResourceListView.as_view(), name='resources-list'),
    path('forums/', ForumPostListView.as_view(), name='forum_post_list'),
    path('forums/create/', ForumPostCreateView.as_view(), name='forum_post_create'),
    path('forums/<int:pk>/', ForumPostDetailView.as_view(), name='forum_post_detail'),
    # path('comment/create/<int:post_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('forums/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('change_password/', views.PasswordChangeView.as_view(template_name = "registration/password_change.html"), name="change-password"),
    path('password_success/', views.password_success, name="password_success"),
    path('ussd_callback/', ussd_callback, name='ussd_callback'),


   
]



