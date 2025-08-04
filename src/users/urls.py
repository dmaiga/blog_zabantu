from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.create_user_view, name='create_user'),

    path('list/', views.user_list_view, name='user_list'),
    path('<int:id>/', views.user_detail_view, name='user_detail'),
    path('create_member/', views.create_member_view, name='create_member'),


]