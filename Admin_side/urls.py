from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.adminLogin,name="adminLogin"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('customers/',views.customers,name='customers'),
    path('block/<int:pk>/',views.block,name='block'),
    path('unblock/<int:pk>/',views.unblock,name='unblock'),
    
]