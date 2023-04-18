from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.connect_to_drone, name='connect'),
    path('send/', views.send_message, name='send'),
    path('receive/', views.receive_message, name='receive'),
    path('control/', views.control, name='control'),
]
