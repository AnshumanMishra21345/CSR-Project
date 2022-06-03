from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, auth
from django.contrib import messages #to display error messages
from django.urls import reverse
import time
from validate_email import validate_email#for email validation
def EMAILCHECK(Email):
    return validate_email(Email,verify=True)

attempts=0#no of attempts made
WAIT=False#Condition that idicates whether if the User is to wait

# Create your views here.
def home(request): # view for homepage
    return render(request, "main/home.html")

def signup_page(request): # view for general signup page
    return render(request, "main/signuppage.html")

def company_signup_page(request): # view for copany signup page
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        password_check= request.POST['password_check']
        number_of_employees= request.POST['number_of_employees']
        capital_available= request.POST['capital_available']
        phone_no= request.POST['phone_no']
        email= request.POST['email']
        address= request.POST['address']
        description= request.POST['description']
        fname= request.POST['fname']
        lname= request.POST['lname ']
        r_email= request.POST['r_email ']
        r_phone_no= request.POST['r_phone_no ']

        if password==password_check: #to check if confirm password option works
            if len(password) < 5:                #to check password length
                messages.info(request, "Password too short. Atleast 5 characters are required.")
                return redirect('/Company-sign-up-page')
            elif len(password) > 50:             #to check password length
                messages.info(request, "Password too long. Atmost 50 characters are required.")
                return redirect('/Company-sign-up-page')
            elif User.objects.filter(username=username).exists(): #to check if the username already exists
                messages.info(request, "Username taken.")
                return redirect('/Company-sign-up-page')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Company Email taken.")
                return redirect('/Company-sign-up-page')
            elif CompRep.objects.filter(r_email=r_email).exists():
                messages.info(request, "Representative email taken.")
                return redirect('/Company-sign-up-page')
            elif not EMAILCHECK(email):
                messages.info(request, "Company Email invalid.")
                return redirect('/Company-sign-up-page')
            elif not EMAILCHECK(r_email):
                messages.info(request, "Representative email invalid.")
                return redirect('/Company-sign-up-page')
            else:
                user=User.objects.create_user(username=username, password= password, email=email, first_name=fname, last_name=lname) #default table created django
                user.save()
                comp= CompanyTable( #storing the appropriate details in company table
                    company_name=username,
                    no_of_employees= number_of_employees,
                    phone=phone_no,
                    email=email,
                    address= address,
                    description= description,
                    cap_available= capital_available
                )
                comp.save()
                rep= CompRep( #storing the appropriate details in representative table
                    company_id = comp,
                    fname = fname,
                    lname = lname,
                    r_phone = r_phone_no,
                    r_email = r_email

                )
                rep.save()
                
        else:
            messages.info(request, "Passwords not matching.") #returns error message
            return redirect('/Company-sign-up-page')

    else:
        return render(request, "registration/compsignuppage.html")

def ngo_signup_page(request): # view for ngo signup page
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        password_check= request.POST['password_check']
        number_of_employees= request.POST['number_of_employees']
        capital_reqd= request.POST['capital_reqd']
        phone_no= request.POST['phone_no']
        email= request.POST['email']
        address= request.POST['address']
        description= request.POST['description']
        fname= request.POST['fname']
        lname= request.POST['lname ']
        r_email= request.POST['r_email ']
        r_phone_no= request.POST['r_phone_no ']

        if password==password_check:
            if len(password) < 5:      #to check password length
                messages.info(request, "Password too short. At least 5 characters are required.")
                return redirect('/NGO-sign-up-page')
            elif len(password) > 50:   #to check password length
                messages.info(request, "Password too long. At most 50 characters are required.")
                return redirect('/NGO-sign-up-page')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username taken.")
                return redirect('/NGO-sign-up-page')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "NGO Email taken.")
                return redirect('/NGO-sign-up-page')
            elif NGORep.objects.filter(r_email=r_email).exists():
                messages.info(request, "Representative email taken.")
                return redirect('/Company-sign-up-page')
            elif not EMAILCHECK(email):
                messages.info(request, "NGO Email invalid.")
                return redirect('/Company-sign-up-page')
            elif not EMAILCHECK(r_email):
                messages.info(request, "Representative email invalid.")
                return redirect('/Company-sign-up-page')
            else:
                user=User.objects.create_user(username=username, password= password , email=email, first_name=fname, last_name=lname) #password will be hashed in table
                user.save()
                print("User created.")
                ngo= NGOTable( 
                    ngo_name=username,
                    no_of_employees= number_of_employees,
                    phone= phone_no,
                    email=email,
                    address= address,
                    description= description,
                    min_cap_reqd= capital_reqd
                )
                ngo.save()
                rep= NGORep(
                    ngo_id = ngo,
                    fname = fname,
                    lname = lname,
                    r_phone = r_phone_no,
                    r_email = r_email

                )
                rep.save()
        else:
            messages.info(request, "Passwords not matching.") #returns error message
            return redirect('/NGO-sign-up-page')

    else:
        return render(request, "registration/ngosignuppage.html")



def login(request):
    global WAIT,attempts
    attempts+=1
    if WAIT==True:#If the user is to be made to wait, a timer for 30 seconds is set while the user is denied any controls
        time.sleep(30)#Become inactive for 30 secs
        WAIT=False;Attempts=0
        return render(request,"registration/login.html",{"WAIT":False})
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']

        user= auth.authenticate(username=username,password=password) #default django authentication protocol that we are calling
        if user is not None:
            auth.login(request,user) #django function allows you to log in
            return redirect(f"/dashboard/{username}")
            attempts=0

        else:
            if attempts>5: #If more than 5 attempts are made, the user's panel is frozen for 30 seconds
                messages.info(request,"You have exceeded 5 attempts of logging in. Please hit refresh to begin cooldown timer.")
                WAIT=True
                return render(request,"registration/login.html",{'WAIT':True})
   

            messages.info(request, "Username or password is incorrect.")
            return redirect("/login")
    else:
        return render(request, "registration/login.html")


def dashboard(request, username):
        try:
            data= CompanyTable.objects.get(company_name=username)
            return render(request, "main/dashboard.html", {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address
            })
        except:
            data= NGOTable.objects.get(ngo_name=username)
            return render(request, "main/dashboard.html", {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address
            })



def logout(request):
    auth.logout(request)#default django logout function
    return redirect('')



    


