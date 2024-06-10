from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.adminLogin,name="adminLogin"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('customers/',views.customers,name='customers'),
    path('block/<int:pk>/',views.block,name='block'),
    path('unblock/<int:pk>/',views.unblock,name='unblock'),
    path('category/',views.category,name='category'),
    path('addCategory/',views.addCategory,name='addCategory'),
    
    
    # path('products/<int:category_id>/<int:subcategory_id>/', views.as_view(), name='product_list_by_category'),
]