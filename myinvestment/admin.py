from django.contrib import admin
from .models import Profile,InvestmentPlan,purchased,Withdrawl_Request
class PurchasedInline(admin.TabularInline):
    model = purchased
    extra = 0 
class WithdrawlInline(admin.TabularInline):
    model = Withdrawl_Request
    extra = 0 
class ProfileAdmin(admin.ModelAdmin):
    inlines = [PurchasedInline,WithdrawlInline]
     

admin.site.register(Profile,ProfileAdmin),
admin.site.register(InvestmentPlan),
admin.site.register(purchased),
admin.site.register(Withdrawl_Request)

# Register your models here.
