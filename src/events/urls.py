from django.urls import path
from .views import (
    event_list,
    event_detail,
    event_create,
    event_update,
    event_delete,
)

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:id>/', event_detail, name='event_detail'),
    path('nouveau/', event_create, name='event_create'),
    path('<int:id>/modifier/', event_update, name='event_update'),
    path('<int:id>/supprimer/', event_delete, name='event_delete'),
]

