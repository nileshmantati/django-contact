from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('home/', home, name='home'),
    path('<int:pk>/', home, name='home'), 
    path('contact/', contact, name='contact'),
    path('contact/<int:pk>/', getsingledata, name='getsingledata'),
    path('edit/<int:pk>/', edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', delete_contact, name='delete_contact'),
    path('status/<int:pk>/', update_status, name='update_status'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
