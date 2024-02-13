from django.shortcuts import render,redirect,HttpResponse

from myinvestment.models import Profile,InvestmentPlan,purchased,Withdrawl_Request
from myinvestment.forms import SignUpForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,get_user
from django.contrib.auth.models import User
def index(request,*args,**kwargs):
    plans=InvestmentPlan.objects.all()
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
   

    return render(request,'index.html',{'plans':plans})
 
def signup(request):
    
    profile_id=request.session.get('ref_profile')
    print('id', profile_id)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile=Profile.objects.get(id=profile_id)
                instance=form.save()
                register_user=User.objects.get(id=instance.id)
                register_profile=Profile.objects.get(user=register_user)
                register_profile.recommended_by=recommended_by_profile.user
                register_profile.save()
            
            user = form.save()
            login(request, user)

            return redirect('dashboard')
    else:
        form = SignUpForm()
        print('error')

    return render(request, 'signup.html', {'form': form})

