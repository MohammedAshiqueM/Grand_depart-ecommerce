from django.shortcuts import render,redirect
from . form import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
# from django.core.validators import validate_email,EmailValidator
import re


########################## function for login & singUp ###############################
@never_cache
def userLogin(request):
    # print("Submit value:", request.POST.get('submit'))

    # if request.user.is_authenticated:
    #     return redirect('userHome') 
    
    active_form = 'login'  # Default active form
    print("Initial active_form:", active_form)

    def clean_email(email):
        mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(mail_regex, email):
            return email
        else:
            raise ValidationError("Invalid email format")

    def clean_password(password):
        if len(password) < 8:
            raise ValidationError("Password should contain at least 8 characters.")
        if not re.search("[A-Z]", password):
            raise ValidationError("Password should contain at least one uppercase letter.")
        if not re.search("[a-z]", password):
            raise ValidationError("Password should contain at least one lowercase letter.")
        if not re.search("[0-9]", password):
            raise ValidationError("Password should contain at least one digit.")
        if not re.search("[@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password should contain at least one special character.")
        return password

    if request.method == 'POST':
        if request.POST.get('submit') == 'login_form':
        ## login the user
        
            username = request.POST.get('loginUsername')
            password = request.POST.get('loginPassword')
            active_form = 'login'

            if not username:
                messages.error(request, "Enter the Email")
            elif not password:
                messages.error(request, "Enter the Password")
            else:
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.error(request, "Invalid Email Id or Password")
                else:
                    auth_login(request, user)
                    return redirect('userHome')

        elif request.POST.get('submit') == 'signup_form':
            ## signUp new user
            
            signUp_username = request.POST['signupUsername']
            signUp_email = request.POST['signupEmail']
            signUp_password1 = request.POST['signupPassword']
            signUp_password2 = request.POST['signupConfirmationPassword']
            active_form = 'signup'
            
            if User.objects.filter(username=signUp_username).exists():
                messages.error(request, f"User name '{signUp_username}' is already taken")
            elif User.objects.filter(email=signUp_email).exists():
                messages.error(request, f"Mail Id '{signUp_email}' already has an account")
            elif signUp_password1 != signUp_password2:
                messages.error(request, "Passwords do not match")
            else:
                    if not signUp_username:
                        messages.error(request, "Enter the username")
                    elif not signUp_email:
                        messages.error(request, "Enter the email")
                    elif not signUp_password1:
                        messages.error(request, "Enter the Password")
                    elif not signUp_password2:
                        messages.error(request, "Enter the Confirmation Password")
                    else:
                
                        try:
                            clean_email(signUp_email)
                            clean_password(signUp_password1)
                        except ValidationError as e:
                            messages.error(request, e.message)
                        else:
                            user = User.objects.create_user(username=signUp_username, email=signUp_email)
                            user.set_password(signUp_password1)
                            user.save()
                            messages.success(request, f"New user '{signUp_username}' is created")
                            return redirect('userLogin')

    print("Final active_form:", active_form)
    return render(request, "login.html", {'active_form': active_form})

########################## function for home page ############################
@login_required(login_url='userLogin')
@never_cache
def userHome(request):
    if request.user.is_authenticated:
        return render(request,"home.html")

########################## function for logout ############################
def logout(request):
    auth_logout(request)
    return redirect('userLogin')
