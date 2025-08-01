from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model,logout
from django.shortcuts import redirect

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return '/users/admin-dashboard/'
        else:
            return '/users/member-dashboard/'

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('member_dashboard')
    return render(request, 'users/admin_dashboard.html')

@login_required
def member_dashboard(request):
    return render(request, 'users/admin_dashboard.html')
