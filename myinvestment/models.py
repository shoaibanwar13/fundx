from django.db import models
from django.contrib.auth.models import User
from .utlis import generate_ref_code

     
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=5,blank=True)
    recommended_by=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="ref_by")
     
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now=True)
    balance=models.IntegerField(default=0)
    withdrawl_amount=models.IntegerField(default=0)
    commission=models.IntegerField(default=0)

    def __str__(self) :

        return  f"{self.user.username}-{self.code}"
    def get_recommended_profile(self):
        query=Profile.objects.all()
        my_recs=[]
        for profile in query:
            if profile.recommended_by==self.user:
                my_recs.append(profile)
        return my_recs
    
    def save(self, *args, **kwargs):
        if self.code=="":
            code=generate_ref_code()
            self.code=code
        super().save(*args, **kwargs)


class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(blank=True, null=True ,default=0)
    daily_return = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_return = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    referral_commission = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class purchased(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved')
    )
    user = models.ForeignKey(User, related_name='purchase', blank=True, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    plan_name=models.CharField(max_length=100,null=True)
    pay_method=models.CharField(max_length=30)
    trans_id=models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    screenshot=models.FileField(upload_to='files',blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_return=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name_plural='Purchased'
        ordering = ('-created_at',)
   
    
    def __str__(self):
        return self.plan_name

class Withdrawl_Request(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Paid'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Paid')
    )
    user = models.ForeignKey(User,  blank=True, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    pay_method=models.CharField(max_length=30)
    account_no=models.CharField(max_length=50)
    account_title=models.CharField(max_length=50)
    #bank=models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(  default=0)

    def __str__(self):
        return self.account_title
     


# Create your models here.
