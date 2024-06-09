from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.adminLogin,name="adminLogin"),
    path('dashboard/',views.dashboard,name='dashboard')
    
]