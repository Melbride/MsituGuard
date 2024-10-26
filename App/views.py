from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Profile, Resource, EmergencyContact,Alert, ResourceRequest, ForumPost, Comment #Post
from .forms import UserRegistrationForm,  ResourceForm, AlertForm, ProfileForm,  ResourceRequestForm, ForumPostForm,  CommentForm,FormComment, EditProfileForm, PasswordChangingForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CustomUserCreationForm

 
# Create your views here.

class HomeView( LoginRequiredMixin, TemplateView):
    # model = Profile
    template_name = 'App/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alerts'] = Alert.objects.all()
        context['resources'] = Resource.objects.all()
        
        if self.request.user.is_authenticated:
            try:
                context['profile'] = self.request.user.profile
            except Profile.DoesNotExist:
                context['profile'] = None
        
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ResourceListView(ListView):
    model = Resource
    template_name = 'App/resource_list.html'
    context_object_name = 'resources'



class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'App/resource_form.html'
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'App/resource_form.html'
    success_url = reverse_lazy('resource_list')


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'App/resource_confirm_delete.html'
    success_url = reverse_lazy('resource_list')


class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'App/resource_detail.html' 
    context_object_name = 'resource'


class EmergencyContactListView(ListView):
    model = EmergencyContact
    template_name = 'App/contact_list.html'
    context_object_name = 'contacts'
    

class ProfileDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Profile
    form_class = ProfileForm
    template_name = 'App/profile_detail.html'
    success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated successfully.")
        return redirect(self.get_success_url())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form) 
        

class AlertListView(ListView):
    model = Alert
    template_name = 'App/alert_list.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile-detail', kwargs={'pk': profile.pk}))
        else:
            # Handle form errors or render the form with errors
            context = self.get_context_data(object=profile, form=form)
            return self.render_to_response(context)

    
class AlertCreateView(CreateView):
    model = Alert
    form_class = AlertForm
    template_name = 'App/alert_form.html'
    success_url = reverse_lazy('latest_alerts')

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class AlertUpdateView(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'App/alert_form.html'
    success_url = reverse_lazy('alert_list')

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)  

        
class LatestAlertsView(ListView):
    model = Alert
    template_name = 'App/latest_alerts.html'  
    context_object_name = 'alerts'

    def get_queryset(self):
        alerts =  Alert.objects.filter(is_approved=True).order_by('-date_created')[:10] 
        logger.debug(f'Latest alerts retrieved: {alerts}')  # Log the alerts
        return alerts

   

class AlertDetailView(DetailView):
    model = Alert
    template_name = 'App/alert_detail.html'
    context_object_name = 'alert'

@login_required
def remove_profile_picture(request):
    profile = request.user.profile
    profile.profile_picture.delete()
    profile.save()
    return redirect('profile_detail')


class ResourceRequestCreateView(CreateView):
    model = ResourceRequest
    form_class = ResourceRequestForm
    template_name = 'App/request_resource.html'
    success_url = reverse_lazy('resource_requests')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ResourceRequestListView(LoginRequiredMixin,ListView):
    model = ResourceRequest
    template_name = 'App/resource_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ResourceRequest.objects.filter(user=self.request.user)

class UseRegisterView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        profile_instance = form.save(commit=False)
        profile_instance.save()
        return super().form_valid(form)


class ForumPostListView(ListView):
    model = ForumPost
    template_name = 'App/forum_post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    form_class = ForumPostForm
   
class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'App/forum_post_create.html'
    success_url = reverse_lazy('forum_post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'App/forum_post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class AddCommentView(CreateView):
    model = Comment
    form_class = FormComment
    template_name = 'App/add_comment.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']

        return super().form_valid(form)
    success_url = reverse_lazy('home')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'login'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "registration/password_change_success.html")



class profile(LoginRequiredMixin, generic.View):
    model = User
    login_url = 'login'
    template_name = "App/profile.html"

    def get(self, request, user_name):
        user_related_data = User.objects.filter(author__username=user_name)[:6]
        user_profile_data = Profile.objects.get(user=request.user.id)
        context = {
            "user_related_data": user_related_data,
            'user_profile_data': user_profile_data
        }
        return render(request, self.template_name, context)


class ApprovedAlertListView(ListView):
    model = Alert
    template_name = 'App/approved_alerts.html'  # The template where alerts will be rendered
    context_object_name = 'approved_alerts'

    def get_queryset(self):
        approved_alerts = Alert.objects.filter(is_approved=True)
        logger.debug(f'Approved alerts retrieved: {approved_alerts}')  # Log the alerts
        return approved_alerts



# class ApprovedResourceListView(ListView):
#     model = ResourceRequest
#     template_name = 'resources/resources.html'  # Your template to display the list
#     context_object_name = 'resources'  # This sets the context variable name in the template
    
#     # Only show approved resources
#     def get_queryset(self):
#         return ResourceRequest.objects.filter(is_approved=True)






from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.models import User
from .models import Profile  # Assuming Profile model is in the same app

user_sessions = {}

logger = logging.getLogger(__name__)

def register_user(username, password, phone_number):
    if User.objects.filter(username=username).exists():
        return False  # Username already exists
    if Profile.objects.filter(phone_number=phone_number).exists():
        return False  # Phone number already registered
    
    # Create the user
    user = User.objects.create_user(username=username, password=password)
    
    # Create a new profile
    Profile.objects.create(user=user, phone_number=phone_number)
    return True  # Registration successful

def authenticate_user(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return True
    except User.DoesNotExist:
        return False
    return False

@csrf_exempt
def ussd_callback(request):
    logger.info("Request Headers: %s", request.headers)
    logger.info("Request Body: %s", request.body)
    logger.info("Request Method: %s", request.method)
    logger.info("Current session state: %s", user_sessions)

    # Check if the request method is POST
    if request.method != "POST":
        return HttpResponse("Bad Request: Expected POST method", status=400)

    # Initialize the response variable
    response = "END Invalid request. Please try again."

    # Get parameters from the request
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text', '')  # Default to an empty string

    logger.info("Parameters: sessionId=%s, serviceCode=%s, phoneNumber=%s, text=%s", session_id, service_code, phone_number, text)

    input_steps = text.split('*')
    logger.info("Input steps: %s", input_steps)

    if text == '':
        # Initial welcome message for all users
        response = "CON Welcome to the Crisis Communication Platform\n"
        response += "1. Latest Alerts\n"
        response += "2. Request a Resource\n"
        response += "3. Share a Resource\n"
        response += "4. Volunteer Opportunities\n"
        response += "5. Emergency Contacts\n"
        response += "6. View Resources\n"
        response += "7. Your Profile\n"
        response += "8. About the Platform\n"
        response += "9. Register/Login\n"
        response += "0. Exit"

    elif input_steps[0] == '1':
        response = "END Here are the latest alerts:\n"  # Logic to fetch and display alerts

    elif input_steps[0] == '2':  # Request a Resource flow
        if len(input_steps) == 1:
            # Step 1: Ask for the type of resource
            response = "CON Request a Resource:\nPlease enter the type of resource you need:"
        elif len(input_steps) == 2:
            # Step 2: Ask for a description
            resource_type = input_steps[1]
            response = f"CON You entered: {resource_type}\nPlease provide a brief description of the resource:"
        elif len(input_steps) == 3:
            # Step 3: Ask for location
            resource_description = input_steps[2]
            response = f"CON Description: {resource_description}\nPlease provide your location:"
        elif len(input_steps) == 4:
            # Step 4: Confirm submission
            location = input_steps[3]
            resource_type = input_steps[1]
            resource_description = input_steps[2]
            response = f"END Resource Request Submitted Successfully!\nResource type: {resource_type}\nDescription: {resource_description}\nLocation: {location}\nWe will process your request soon."
        else:
            response = "END Invalid input. Please try again."

    elif input_steps[0] == '3':  # Share a Resource
        response = "CON Share a Resource:\nPlease enter the details of the resource you're sharing."
    elif input_steps[0] == '4':  # Volunteer Opportunities
        response = "CON Volunteer Opportunities:\nPlease enter your availability."
    elif input_steps[0] == '5':  # Emergency Contacts
        response = "CON Emergency Contacts:\n1. Local Disaster Response Team\n2. Police\n3. Ambulance"
    elif input_steps[0] == '6':  # View Resources
        response = "CON View Resources:\n1. Food\n2. Clothes"
    elif input_steps[0] == '7':  # Your Profile
        response = "CON Your Profile:\n1. View Details\n2. Edit Profile"
    elif input_steps[0] == '8':  # About the Platform
        response = "END About the Platform:\nThis platform helps communities during crises by sharing resources and sending alerts."
    elif input_steps[0] == '9':  # Register/Login
        if len(input_steps) == 1:
            # Step 1: Show login/registration options
            response = "CON Welcome to the Crisis Communication Platform\n"
            response += "1. Register\n"
            response += "2. Login\n"
        elif input_steps[1] == '1':  # Registration Flow
            if len(input_steps) == 2:
                response = "CON Register:\nPlease enter your username:"
            elif len(input_steps) == 3:
                response = "CON Enter your password:"
            elif len(input_steps) == 4:
                response = "CON Confirm your password:"
            elif len(input_steps) == 5:
                username = input_steps[2]
                password = input_steps[3]
                confirm_password = input_steps[4]

                if password != confirm_password:
                    response = "END Passwords do not match. Please try again."
                else:
                    registration_success = register_user(username=username, password=password, phone_number=phone_number)

                    if registration_success:
                        response = f"END Registration successful! Welcome, {username}."
                    else:
                        response = "END Username already taken. Please try a different username."
        elif input_steps[1] == '2':  # Login Flow
            if len(input_steps) == 2:
                response = "CON Login:\nPlease enter your username:"
            elif len(input_steps) == 3:
                response = "CON Enter your password:"
            elif len(input_steps) == 4:
                username = input_steps[2]
                password = input_steps[3]

                if authenticate_user(username=username, password=password):
                    response = "CON Welcome back, {}!\n".format(username)
                    response += "1. Latest Alerts\n"
                    response += "2. Request a Resource\n"
                    response += "3. Share a Resource\n"
                    response += "4. Volunteer Opportunities\n"
                    response += "5. Emergency Contacts\n"
                    response += "6. View Resources\n"
                    response += "7. Your Profile\n"
                    response += "8. About the Platform\n"
                    response += "0. Exit"
                else:
                    response = "END Invalid login. Please check your credentials."

    elif text == '0':
        response = "END Thank you for using the Crisis Communication Platform. Goodbye!"

    return HttpResponse(response, content_type='text/plain')
