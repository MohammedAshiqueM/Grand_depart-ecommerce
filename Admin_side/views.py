from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import (
    User, Address, PaymentType, PaymentMethod, Category,SubCategory,
    Variation, VariationOption, Product, ProductConfiguration,
    Cart, CartItem, ShippingMethod, OrderStatus, Order, OrderLine, Review, Promotion, PromotionCategory
)


# Create your views here.
@never_cache
def adminLogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        # if not User.objects.filter(email=username).exists():
        #     messages.error(request,'Account not found')
        #     print("1",messages.error)
        #     return redirect('adminLogin')
        user = authenticate(username = username,password = password)
        if user is None:
            messages.error(request,"Invalid username or password")
            return redirect('adminLogin')
        elif user and user.is_superuser:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,f"{user} have no access to this page")
            return redirect('adminLogin')
    return render(request,'adminLogin.html')

# @login_required(login_url='adminLogin')
# @never_cache
def dashboard(request):
    # if not request.user.is_superuser:
    #     return HttpResponseForbidden("You do not have access to this page.")
    return render(request,'dashboard.html')

def customers(request):
    if 'value' in request.GET:
        credential = request.GET['value']
        data = User.objects.filter(Q(username__icontains=credential) | Q(email__icontains=credential))
        context = {'data':data}
    else:
        data = User.objects.all()
        print(f"SQL Query: {str(data.query)}") 
        print(list(data))
        context = {'data':data}
        print(data)
    return render(request,'customers.html',context)

def block(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Internal server error'})

def unblock(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Internal server error'})
    
    

def category(request):
    if 'value' in request.GET:
        credential = request.GET['value']
        parent = Category.objects.filter(Q(name__icontains=credential))
        sub = SubCategory.objects.filter(Q(name__icontains=credential) | Q(category__name__icontains=credential))
        context = {"parent":parent,"sub":sub}
    else:
        parent = Category.objects.all()
        sub = SubCategory.objects.all()
        context = {"parent":parent,"sub":sub}
    return render(request,"category.html",context)

def addCategory(request):
        data = Category.objects.all()
        if request.method == 'POST':
            print("outside")
            if request.POST.get('submit') == 'main':
                print("inside")
                category = request.POST.get('categoryName')
                print(category)
                if not category:
                    messages.error(request, "Enter a Category name")
                    return redirect('addCategory')
                elif len(category) < 3:
                    messages.error(request,"Category name must have atleast 3 letters")
                    return redirect('addCategory')
                else:
                    newCategory = Category.objects.create(name=category)
                    newCategory.save()
                    messages.success(request,f"New cagetory {newCategory} is created")
                return redirect('category')
            elif request.POST.get('submit') == 'sub':
                sub_category = request.POST.get('subCategory')
                selected = request.POST.get('parentCategory')
                print(sub_category,selected)
                if not sub_category:
                    messages.error(request, "Enter a Subcategory name")
                    return redirect('addCategory')
                elif len(sub_category) < 3:
                    messages.error(request,"Subcategory name must have atleast 3 letters")
                    return redirect('addCategory')
                elif not selected :
                    messages.error(request,f"Should select one parent class for subclass {sub_category}")
                    return redirect('addCategory')
                else:
                    parent = Category.objects.get(id=selected)
                    newSub = SubCategory.objects.create(name=sub_category,category=parent)    
                    newSub.save()
                    messages.success(request,f"New cagetory {newSub} is created")
                return redirect('category')
        return render(request,"addCategory.html",{"data":data})


# class ProductListView(ListView):
#     model = Product
#     template_name = 'product_list.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         category_id = self.kwargs.get('category_id')
#         subcategory_id = self.kwargs.get('subcategory_id')
#         queryset = Product.objects.all()

#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         if subcategory_id:
#             queryset = queryset.filter(subcategory_id=subcategory_id)

#         return queryset