from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import JsonResponse



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
        context = {'data':data}
    return render(request,'customers.html',context)

def block(request,pk):
    user = User.objects.get(pk=pk)
    user.is_active = False
    data = User.objects.all()
    context = {'data':data}
    user.save()
    return JsonResponse({'success': True})

def unblock(request,pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    data = User.objects.all()
    context = {'data':data}
    return JsonResponse({'success': True})