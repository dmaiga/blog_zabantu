from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from .forms import CustomMemberCreationForm

#--------------------------------------------------------------------
#08_08
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from .models import CustomUser
from .forms import ProfileEditForm, CustomPasswordChangeForm

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil a été mis à jour avec succès.")
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Votre mot de passe a été changé avec succès.")
        return super().form_valid(form)
#_______________________________________________________________
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
              
                return redirect('dashboard')
            else:
                messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html', {'user': request.user})

@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur créé avec succès!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_list_view(request):
    users = CustomUser.objects.all().order_by('role', 'last_name')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, 'users/user_detail.html', {'user_detail': user})

@login_required
def create_member_view(request):
    if request.user.role not in ['admin', 'moderateur']:
        return redirect('login')

    if request.method == 'POST':
        form = CustomMemberCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le membre a été créé avec succès.")
            return redirect('user_list')  # ou admin_dashboard
    else:
        form = CustomMemberCreationForm()
    return render(request, 'users/create_member.html', {'form': form})

