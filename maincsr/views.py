from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, auth
from django.contrib import messages #to display error messages
from django.urls import reverse
import time,datetime
from django.conf import settings
from django.core.mail import send_mail
import snoop

client = ''#stores current user's username
connto=''#stores username of company/NGO to which a connection is to be sent
conntype=''#stores values 'NGO' or 'Company' to help determine the recipient of the connection 
cttype = ''#stores type of client
attempts=0#no of attempts made
WAIT=False#Condition that indicates whether if the User is to wait

def home(request): # view for homepage
    
    return render(request, "main/home.html")

def signup_page(request): # view for general signup page
    
    return render(request, "main/signuppage.html")

def login_request(request):
    global WAIT,attempts
    if WAIT==True:#If the user is to be made to wait, a timer for 30 seconds is set while the user is denied any controls
        time.sleep(30)#Become inactive for 30 secs
        WAIT=False;attempts=0
        return render(request,"registration/login.html",{"WAIT":False})
    if request.method=='POST':
        attempts+=1
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password) #default django authentication protocol that we are calling
        global client
        client = username
        if user is not None:
            login(request,user) #django function allows you to log in
            return redirect(f"/dashboard/{username}")
            attempts=0

        else:
            if attempts>=3: #If more than 3 attempts are made, the user's panel is frozen for 30 seconds
                messages.info(request,"You have exceeded 3 attempts of logging in. Please hit refresh and wait for 30 seconds")
                WAIT=True
                return render(request,"registration/login.html",{'WAIT':True})
   

            messages.info(request, "Username or password is incorrect.")
            return redirect("/login")
    else:
        return render(request, "registration/login.html")

@snoop
def logout_request(request):
    
    logout(request)#default django logout function
    return redirect('/home')

@snoop
def company_signup_page(request): # view for company signup page
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

                subject = "Registration has been completed."
                msg1 = f"Hello {username}!!!,\nThank you for creating an account on our Platform. \n\nWe look forward to seeing your generosity."
                msg2 = f"\nHope you find it easy to find the right charity.\n--The CSR Platform Team."
                message = msg1+msg2
                recipient_list = [email,r_email]
                mail(subject,message,recipient_list)
        else:
            messages.info(request, "Passwords not matching.") #returns error message
            return redirect('/Company-sign-up-page')
        return redirect('/login')

    else:
        return render(request, "registration/compsignuppage.html")

@snoop
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
        lname= request.POST['lname']
        r_email= request.POST['r_email']
        r_phone_no= request.POST['r_phone_no']
        state = request.POST.get('state') #drop-down box
        sector = request.POST.get('sector')#drop-down box
        pdf=request.FILES.get("cert")
        
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
                return redirect('/NGO-sign-up-page')
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
                    min_cap_reqd= capital_reqd,
                    pdf=pdf,
                    state=state,
                    sectors=sector

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
                subject = 'Registration completed Sucessfully'
                msg1 = f'Hello {username}!!!,\nThank you for creating an account with our Platform.'
                msg2 = '\n\nWe look forward to seeing you help everyone.\n--The CSR Platform Team'
                message = msg1 + msg2
                recipient_list = [email,r_email]
                mail(subject,message,recipient_list)
        else:
            messages.info(request, "Passwords not matching.") #returns error message
            return redirect('/NGO-sign-up-page')

        return redirect("/login")
    else:
        return render(request, "registration/ngosignuppage.html")

@snoop
@login_required(login_url='/login')
def dashboard(request, username):
    global client #client variable may get deleted after any error is encountered, thus it saved again just in case
    client=username
    
    if request.method=="GET": #edit 3
        users=[] 
        try:#COMPANY DASHBOARD
            ngos=[]
            data = CompanyTable.objects.get(company_name=username)
            #For display purposes, entire content is broken into lines of length 15
            """descwords=data.description.split()#List of all words in description
            for i in range(len(descwords)):
                Line=""
                for j in range(len(descwords[i])):
                    Line+=descwords[i][j]
                    if j%5==0 and j%3==0 and j!=0: #Checking if it is a multiple of fifteen
                       Line+=" "
                descwords[i]=Line
               

            data.description=""
            if len(descwords)==1:
                data.description=descwords[i]
            else:
                for k in descwords:
                    data.description+=k+" "
            print(data.description,descwords)""" 

            for i in NGOTable.objects.values_list('ngo_name'):
                    ngos.append(i[0])
            connpendC,connpendN,connacc=[],[],[] # connection pending for company, pending for NGO and  connection accepted
            for k in Connections.objects.values_list('company_name','ngo_name','status'):#Queryset of connections directed to user
                    if k[2]=="PendingC":
                        if k[0]==username:
                           connpendC.append(k[1])  
                    elif k[2]=="PendingN":
                        if k[0]==username:
                           connpendN.append(k[1]) 
                    elif k[2]=="Accepted":
                        if k[0]==username:
                           connacc.append(k[1])
            return render(request, "main/dashboard.html", {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address,
            'users': users,
            'org_name': username,
            'ngos':ngos,
            'connpendC':connpendC,#Pending connections on Company end
            'connpendN':connpendN,#Pending connections on NGO end
            'connacc':connacc #Accepted connections
            })
        except:#NGO DASHBOARD
            comp=[]
            data= NGOTable.objects.get(ngo_name=username)
            for i in CompanyTable.objects.values_list('company_name'):
                comp.append(i[0])
            connpendC,connpendN,connacc=[],[],[]# connection pending for company, pending for NGO and  connection accepted
            for k in Connections.objects.values_list('ngo_name','company_name','status'):#Queryset of connections directed to user
                    if k[2]=="PendingC":
                        if k[0]==username:
                           connpendC.append(k[1])  
                    elif k[2]=="PendingN":
                        if k[0]==username:
                           connpendN.append(k[1]) 
                    elif k[2]=="Accepted":
                        if k[0]==username:
                           connacc.append(k[1])
            connections=Connections.objects.filter(ngo_name=username)
            context = {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address,
            'users': users,
            'org_name': username,
            'comp':comp,
            'connpendC':connpendC,#Pending connections on Company end
            'connpendN':connpendN,#Pending connections on NGO end
            'connacc':connacc} #Accepted connections
            if data.pdf != '':
                context['cert'] = data.pdf
            return render(request, "main/dashboard.html",context)

@login_required(login_url='/login')
@snoop
def search(request):
    # the for = in html should match the value in brackets
    if request.method=="POST":
        cat = request.POST.get('category')#'NGO' - States if NGO or company
        orgname = request.POST.get('orgname')#'He'- Basically organisation name
        emp_count = request.POST.get('emp_count')
        cap= request.POST.get('cap')
        state = request.POST.get('state') #drop-down box
        sector = request.POST.get('sector')#drop-down box
        sort_by = request.POST.get('sort_by')#'ngo_name' or 'company_name' 
        order = request.POST.get('order') #- by ascending or descending
        global cttype
        if cat == 'NGO':
            data = NGOTable.objects.filter(ngo_name__icontains = orgname)# i here makes it non case sensitive
            
            data = data.exclude(ngo_name = client)
            for i in data:
                print(i)
            cttype = 'NGO'
            if cap != '':
                data = data.filter(min_cap_reqd__range = (int(cap),int(cap) + 10000))
            if state != 'None':
                data = data.filter(state__exact = state)#exact as the name suggests means exact value
            if sector != 'None':
                data = data.filter(sectors__in = sector)
        elif cat == 'COMPANY':
            data = CompanyTable.objects.filter(company_name__icontains = orgname).exclude(company_name = client)
            cttype = 'Company'
            if cap != '':
                data = data.filter(cap_available__range = (int(cap) ,int(cap) + 10000))
        #replace None by whatever default value is returned by HTML for not filling a column

        if emp_count !='':
            emp_count = int(emp_count)
            data = data.filter(no_of_employees__range = (emp_count - 500,emp_count + 500))# range is the between and 

        if sort_by != 'None':
            if order  == 'Ascending':
                data = data.order_by(sort_by)
            elif order == 'Descending':
                sort_by = '-'+sort_by
                data = data.order_by(sort_by)

        return render(request, 'main/results.html' , {'data': data})#edit1
         #edit 2
    else:
        return render(request, 'main/search.html')  

@login_required(login_url='/login')
def search_result(request,username):
    global conntype 
    global client
    global connto
    connto=username
    status=""
    
    if request.method=="GET": #edit 3
        try:#VIEWING AN COMPANY'S DASHBOARD
            data = CompanyTable.objects.get(company_name=username)
            for a in Connections.objects.values_list('ngo_name','company_name','status'):
                if a[0]==client and a[1]==username:
                       status=a[2]
            conntype="Company"
            return render(request, "main/othprofile.html", {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address,
            'org_name': username,
            'client': client,
            'status':status,
            'conntype':conntype,
            'clienttype':cttype
            })
        except:#VIEWING AN NGO'S DASHBOARD
            data= NGOTable.objects.get(ngo_name=username)
            for a in Connections.objects.values_list('company_name','ngo_name','status'):
                if a[0]==client and a[1]==username:
                       status=a[2]
            conntype="NGO"
            context = {'about': data.description,
            'email': data.email,
            'phone': data.phone,
            'address': data.address,
            'org_name': username,
            'client': client,
            'status':status,
            'conntype':conntype,
            'clienttype':cttype
            }
            if data.pdf != '':
                context['cert'] = data.pdf
            return render(request, "main/othprofile.html", context)
            
@snoop
@login_required(login_url='/login')
def connect(request):
    global connto, client , conntype 
    dtval= datetime.datetime.now()
    if request.method=="POST":
        if conntype=="Company":#If connection request directed to a company
            if 'Acceptance' not in request.POST and 'Refusal' not in request.POST:
                comp=Connections( #storing the appropriate details in connections table
                                ngo_name=client,
                                company_name=connto,
                                initiator=client,
                                status="PendingC",
                                respdate=None,
                                senddate=dtval,
                            )
                comp.save()
            else:
                NGOid=NGOTable.objects.filter(ngo_name=client).values_list('id', flat=True).first()
                NGOemail=NGOTable.objects.get(ngo_name=client).email
                Compid=CompanyTable.objects.filter(company_name=connto).values_list('id', flat=True).first()
                Compemail=CompanyTable.objects.get(company_name=connto).email
                if 'Acceptance' in request.POST:
                    Connections.objects.filter(ngo_name=client,company_name=connto).update(status="Accepted",respdate=dtval)
                    for a in NGORep.objects.values_list('ngo_id_id','fname','lname','r_phone','r_email'):
                        if a[0]==NGOid:
                            for b in CompRep.objects.values_list('company_id_id','fname','lname','r_phone','r_email'):
                                if b[0]==Compid: # This sends an email to ngo if company refuses
                                        subject= "Connection made!"
                                        msg1 = f"Hello {client}!!!,\nThe Company,{connto} has agreed to connect to your NGO."
                                        msg2 = f"\nYou may contact the Company representative whose details are mentioned below"
                                        msg3 = f"\nName : {b[1]} {b[2]}\nphone : {b[3]}\nemail : {b[4]}"
                                        msg4 = f"\nHope our contribution may help your NGO achieve its goals.\n--The CSR Platform Team"
                                        message = msg1+msg2+msg3+msg4
                                        recipient_list = [NGOemail,]
                                        mail(subject,message,recipient_list)

                                        subject = "Connection made!"
                                        msg1 = f"Hello {connto}!!!,\nThe NGO,{client} has agreed to connect to your Company."
                                        msg2 = f"\nYou may contact the NGO representative whose details are mentioned below"
                                        msg3 = f"\nName : {a[1]} {a[2]}\nphone : {a[3]}\nemail : {a[4]}"
                                        msg4 = f"\nHope our contribution may help your Company achieve its goals.\n--The CSR Platform Team"
                                        message = msg1+msg2+msg3+msg4
                                        recipient_list = [Compemail,]
                                        mail(subject,message,recipient_list)
                            
                                        

                elif 'Refusal' in request.POST:
                    Connections.objects.filter(ngo_name=client,company_name=connto).update(status="Refused",respdate=dtval)
                    for a in NGORep.objects.values_list('ngo_id_id','fname','lname','r_phone','r_email'):
                        if a[0]==NGOid:
                            for b in CompRep.objects.values_list('company_id_id','fname','lname','r_phone','r_email'):
                                if b[0]==Compid: # This sends an email to company if ngo refuses
                                        subject= "Connection request denied"
                                        msg1 = f"Hello {connto},\nThe NGO,{client} has denied to connect to your Company."
                                        msg2 = f"\nWe hope you do find another partner NGO.\n--The CSR Platform Team"
                                        message = msg1+msg2
                                        recipient_list = [Compemail,]
                                        mail(subject,message,recipient_list)

        else:#If connection request directed to a NGO
            Compid=CompanyTable.objects.filter(company_name=client).values_list('id', flat=True).first()
            Compemail=CompanyTable.objects.get(company_name=client).email
            NGOid=NGOTable.objects.filter(ngo_name=connto).values_list('id', flat=True).first()
            NGOemail=NGOTable.objects.get(ngo_name=connto).email
            if 'Acceptance' not in request.POST and 'Refusal' not in request.POST:
                ngo=Connections( #storing the appropriate details in connections table
                            ngo_name=connto,
                            company_name=client,
                            initiator=client,
                            status="PendingN",
                            respdate=None,
                            senddate=dtval,
                        )
                ngo.save()
            else:
                if 'Acceptance' in request.POST:
                    Connections.objects.filter(ngo_name=connto,company_name=client).update(status="Accepted",respdate=dtval)
                    for a in CompRep.objects.values_list('company_id_id','fname','lname','r_phone','r_email'):
                        if a[0]==Compid:
                            for b in NGORep.objects.values_list('ngo_id_id','fname','lname','r_phone','r_email'):
                                if b[0]==NGOid: # This sends an email to both ngo and company indicating successful connection
                                        subject = "Connection made!"
                                        msg1 = f"Hello {client}!!!,\nThe NGO,{connto} has agreed to connect to your Company."
                                        msg2 = f"\nYou may contact the NGO representative whose details are mentioned below"
                                        msg3 = f"\nName : {b[1]} {b[2]}\nphone : {b[3]}\nemail : {b[4]}"
                                        msg4 = f"\nHope our contribution may help your Company achieve its goals.\n--The CSR Platform Team"
                                        message = msg1+msg2+msg3+msg4
                                        recipient_list = [Compemail,]
                                        mail(subject,message,recipient_list)

                                        subject= "Connection made!"
                                        msg1 = f"Hello {connto}!!!,\nThe Company,{client} has agreed to connect to your NGO."
                                        msg2 = f"\nYou may contact the Company representative whose details are mentioned below"
                                        msg3 = f"\nName : {a[1]} {a[2]}\nphone : {a[3]}\nemail : {a[4]}"
                                        msg4 = f"\nHope our contribution may help your NGO achieve its goals.\n--The CSR Platform Team"
                                        message = msg1+msg2+msg3+msg4
                                        recipient_list = [NGOemail,]
                                        mail(subject,message,recipient_list)

                                        
                elif 'Refusal' in request.POST: 
                    Connections.objects.filter(ngo_name=connto,company_name=client).update(status="Refused",respdate=dtval)
                    for a in CompRep.objects.values_list('company_id_id','fname','lname','r_phone','r_email'):
                        if a[0]==Compid:
                            for b in NGORep.objects.values_list('ngo_id_id','fname','lname','r_phone','r_email'):
                                if b[0]==NGOid: # This sends an email to ngo if company refuses
                                        subject= "Connection request denied"
                                        msg1 = f"Hello {connto} ,\nThe Company,{client} has denied to connect to your NGO."
                                        msg2 = f"\nWe urge you to keep trying. You shall certainly succeed.\n--The CSR Platform Team"
                                        message = msg1+msg2
                                        recipient_list = [NGOemail,]
                                        mail(subject,message,recipient_list)
                                        

    return redirect(f"/dashboard/{client}")

@snoop
def mail(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,recipient_list,fail_silently=True)
    pass
