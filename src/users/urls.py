from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    CustomLoginView,
    logout_view,
    profile_view,
    admin_dashboard,
    member_dashboard
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', member_dashboard, name='member_dashboard'),
]
