from django.urls import path
from . import views

urlpatterns = [
    path('login_register/', views.access, name='access'),
]