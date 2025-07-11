
from django.urls import path, include
from django.shortcuts import redirect
from . import views
from .views import ussd_callback

from django.contrib.auth import views as auth_views
from .views import UseRegisterView #CustomLoginView
from .views import CustomPasswordResetView
from .views import request_verification  
# from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView

# from .forms import LoginFormWithCaptcha


from .views import(HomeView,   UserLogoutView, ResourceListView, ResourceCreateView,
                   ResourceUpdateView, ResourceDeleteView, ProfileDetailView, 
                   ResourceDetailView, AlertListView, AlertCreateView, AlertUpdateView, AlertDetailView,
                   LatestAlertsView, ResourceRequestCreateView, ResourceRequestListView,
                   ForumPostListView, ForumPostCreateView, ForumPostDetailView,  AddCommentView, UserEditView, ApprovedAlertListView,
                   ApprovedContributeListView, TemplateView)
#,UserRegisterView
                   
urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    # path('', include('django.contrib.auth.urls')), 
    path('register/', UseRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/new/', ResourceCreateView.as_view(), name='resource_create'),
    path('resource/edit/<int:pk>/', ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource_delete'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),

    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('request-verification/', request_verification, name='request_verification'),
    # path('profile/remove_picture/', remove_profile_picture, name='remove_profile_picture'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('alerts/', AlertListView.as_view(), name='alert_list'),
    path('alerts/new/', AlertCreateView.as_view(), name='alert_create'),  # Use alert_create
    path('alert/edit/<int:pk>/', AlertUpdateView.as_view(), name='alert_update'),
    path('latest-alerts/', LatestAlertsView.as_view(), name='latest_alerts'),
    path('alerts/<int:pk>/', AlertDetailView.as_view(), name='alert_detail'),
    path('approved-alerts/', ApprovedAlertListView.as_view(), name='approved_alerts'),
    path('approved-contributes/', ApprovedContributeListView.as_view(), name='approved_contributes'),
    path('request-resource/', ResourceRequestCreateView.as_view(), name='request_resource'),
    path('resource-requests/', ResourceRequestListView.as_view(), name='resource_requests'),
    path('request/success/', TemplateView.as_view(template_name='App/request_success.html'), name='request_success'),
    # path('resources/', ApprovedResourceListView.as_view(), name='resources-list'),
    path('forums/', ForumPostListView.as_view(), name='forum_post_list'),
    path('forums/create/', ForumPostCreateView.as_view(), name='forum_post_create'),
    path('forums/<int:pk>/', ForumPostDetailView.as_view(), name='forum_post_detail'),
    # path('comment/create/<int:post_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('forums/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # path('password/', auth_vie
    # ws.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('change_password/', views.PasswordChangeView.as_view(template_name = "registration/password_change.html"), name="change-password"),
    path('password_success/', views.password_success, name="password_success"),
    path('ussd_callback/', ussd_callback, name='ussd_callback'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        success_url='/password_reset_done/',
        email_template_name='registration/password_reset_email.txt',  
        html_email_template_name='registration/password_reset_email.html'  
    ), name='password_reset'),

    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Redirect old contacts URL to home page footer
    path('contacts/', lambda request: redirect('/#footer-contact')),





    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
   
    # path('login/', CustomLoginView.as_view(), name='login'),

# from django.urls import path
# from django.contrib.auth import views as auth_views

   
   
]



