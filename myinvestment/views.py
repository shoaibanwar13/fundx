from django.shortcuts import render,HttpResponse,redirect
from .forms import SignUpForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,get_user
from .models import Profile,InvestmentPlan,purchased,Withdrawl_Request
from django.db.models import Sum
 
import time
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string






def refral(request,*args,**kwargs):
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())

    return render(request,'index.html')
@login_required
def dashboard(request):
    user_purchase=purchased.objects.filter(user=request.user).values_list('amount',flat=True)
    payout=Profile.objects.filter(user=request.user).values_list('balance',flat=True)
    totalwithdraw=Profile.objects.filter(user=request.user).values_list('withdrawl_amount',flat=True)
    pro=Profile.objects.get(user=request.user)
    payout1=int(pro.balance)
    has_purchase_plans = purchased.objects.filter(user=request.user).exists()
    print(has_purchase_plans)
    totalcom=Profile.objects.get(user=request.user)
    comtotal=totalcom.commission
     
    userbalace=pro.balance==0
    
    print(userbalace)
    total_withdraw=sum(totalwithdraw)
    print(total_withdraw)
    total_payout=sum(payout)
    total=sum( user_purchase)
    total_pending=user_purchase=purchased.objects.filter(user=request.user).values_list('pending',flat=True)
    pending_total=sum(total_pending)
     
    pending=purchased.objects.filter(user=request.user,status='Pending') 
    approve=purchased.objects.filter(user=request.user,status='Approved') 
    
    


    return render(request,'wallet.html',{'user_purchase': user_purchase,'has_purchase_plans':has_purchase_plans,'total':total,'pending':pending,'approved':approve,'pending_total':pending_total,'total_payout':total_payout,'total_withdraw':total_withdraw,'comtotal':comtotal, 'payout1':payout1,'userbalace':userbalace})
@login_required
def purchased_plan (request):
        
        if request.method=="POST":
           Pname=request.POST.get("pname")
           daily_return=request.POST.get("daily")
           pending=request.POST.get("pending")
           pmethod=request.POST.get("pmethod")
           trxid=request.POST.get("trxid")
           sshort=request.FILES['sshort']
           profile=Profile.objects.get(user=request.user)
           inserdata=purchased(user=request.user,profile=profile,plan_name=Pname,pay_method=pmethod,daily_return=daily_return,trans_id=trxid,screenshot=sshort,pending=pending,amount=pending)
           inserdata.save()
           email_subject2 = "New Deposit Arrival For  Investment "
           message2 = render_to_string('SendEmail3.html', {
                    'profile':profile,
                    'pmethod':  pmethod,
                    'trxid':trxid,
                    'amount': pending,
                    'plan_name': Pname,
              
        })
        email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
        email_message2.send()
        messages.success(request, 'Withdrawl Success!! It take 3 to 5 mintue to Arrived in your Account ')

        try:
           user_profile=Profile.objects.get(user=request.user)
           reffferer=user_profile.recommended_by
           if reffferer:
               commission=int(pending)*0.1
               reffferer_profile=Profile.objects.get(user=reffferer)
               reffferer_profile.commission +=commission
               reffferer_profile.balance +=commission
               reffferer_profile.save()
               redirect('dashboard')
           else:
               pass

        except:
           pass

           
               

            
         
    

        
      
        return render(request,'history.html')
def pricing(request):
    plans=InvestmentPlan.objects.all()
    return render(request,'Plans.html',{'plans':plans})
@login_required
def plandetail(request,id):
    detail=InvestmentPlan.objects.filter(id=id).first()
   
    return render(request,'plandetail.html',{'detail': detail})
@login_required
def history(request):
    user_deposit=purchased.objects.filter(user=request.user)
    print(user_deposit)
    approve=purchased.objects.filter(user=request.user,status='Approved') 
    print(approve)
    withdraw=Withdrawl_Request.objects.filter(user=request.user)
    print(withdraw)
    user_purchase=purchased.objects.filter(user=request.user).values_list('amount',flat=True)
    payout=Profile.objects.filter(user=request.user).values_list('balance',flat=True)
    totalwithdraw=Profile.objects.filter(user=request.user).values_list('withdrawl_amount',flat=True)
    pro=Profile.objects.get(user=request.user)
    payout1=int(pro.balance)
      
    totalcom=Profile.objects.get(user=request.user)
    comtotal=totalcom.commission
     
    
    total_withdraw=sum(totalwithdraw)
    print(total_withdraw)
    total_payout=sum(payout)
    total=sum( user_purchase)
    total_pending=user_purchase=purchased.objects.filter(user=request.user).values_list('pending',flat=True)
    pending_total=sum(total_pending)

    paid=Withdrawl_Request.objects.filter(user=request.user,status='Paid')
    print(paid)
    pending=purchased.objects.filter(user=request.user,status='Pending') 
    return render(request,'history.html',{ 'approved':approve, 'user_deposit':user_deposit,'withdraw': withdraw,'paid':paid,'user_purchase': user_purchase,'total':total,'pending':pending,'approved':approve,'pending_total':pending_total,'total_payout':total_payout,'total_withdraw':total_withdraw,'comtotal':comtotal, 'payout1':payout1})
@login_required
def withdraw(request):
    pro=Profile.objects.get(user=request.user)
    payout1=int(pro.balance)
    print(payout1)
     


    if request.method=="POST":
            pmethod=request.POST.get("pmethod")
             
            account_title=request.POST.get("account_title")
            account_no=request.POST.get("account_no")
            withrwal_amount=int(request.POST.get("amount"))
            profile=Profile.objects.get(user=request.user)
            query=Withdrawl_Request(user=request.user, profile=profile,account_title=account_title,account_no=account_no,amount=withrwal_amount,pay_method=pmethod)
            query.save()
            
            
            if withrwal_amount <= int(profile.balance):
                if withrwal_amount >=200:
                    profile.balance -=withrwal_amount
                    profile.withdrawl_amount +=withrwal_amount
                    profile.save()
                    email_subject2 = "Withdrawl Request"
                    message2 = render_to_string('SendEmail2.html', {
                    'profile':profile,
                    'pmethod':  pmethod,
                    'account_title':account_title,
                    'account_no':account_no,
                    'withrwal_amount': withrwal_amount,
              
        })
                    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
                    email_message2.send()
                    messages.success(request, 'Withdrawl Success!! It take 10 to 30 mintue to Arrived in your Account ')
                    redirect('dashboard')
                else:
                     messages.success(request, 'Minimum Withdrawl is PKR 200 ')
                     redirect('dashboard')
                
            if withrwal_amount>profile.balance:
              messages.warning(request, 'Your Withdrwal Request Is Greater Than Available Balance.')
              redirect('dashboard')
              
     

    
    return  redirect('dashboard')
@login_required
def referal(request):
    refer_code=Profile.objects.get(user=request.user)
    recom_code=refer_code.code
    profile=Profile.objects.get(user=request.user)
    my_recs=profile.get_recommended_profile()
    print(my_recs)
    earning=Profile.objects.get(user=request.user)
    my_earning=earning.commission
    print(my_earning)
    print( recom_code)
    return render(request,'Reffral.html',{' recom_code':   recom_code,'my_recs':my_recs,'my_earning':my_earning})
@login_required
def profile(request):
    refer_code=Profile.objects.get(user=request.user)
    recom_code=refer_code.code
    
    return render(request,'Profile2.html',{' recom_code':  recom_code})
 
def contact(request):
     
    
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')



@login_required 
def updteprofile(request):
     if request.method == 'POST':
        user = request.user
        user.username= request.POST.get('name')
        user.save()
        print('save password')
        return redirect('profile')
     return render(request,'password.html')


def check_username(request):
    username=request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
       return  HttpResponse("<div style='color:red;'>  Phone Number Already Used</div>")
    else:
        return HttpResponse("<div style='color:green;'> Phone Number is Available </div>")
def check_email(request):
    email=request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
       return  HttpResponse("<div style='color:red;'>Email Already Exist</div>")
    else:
        return HttpResponse("<div style='color:green;'>Email   is Available </div>")
    

 
    

# Create your views here.
