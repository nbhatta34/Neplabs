from django.contrib import admin
from django.contrib.auth import get_user_model
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Cart, Hospital, LabResult, Order, ProductInCart, Test, UserProfile, VaccineBooking
# Register your models here.
# admin.site.site_header = "Neplabs Admin Portal"

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = [('email'),('username'),('phone')]

    fieldsets = (
        (None, {'fields':('email', 'username', 'password')}),
        ('Personal Information',{'fields':('first_name','last_name', 'phone','gender')}),
        ('Permissions',{'fields':('is_staff','is_superuser', 'is_active')})
    )

admin.site.register(User, UserAdmin)

admin.site.register(Hospital)

admin.site.register(Test)

admin.site.register(LabResult)

admin.site.register(UserProfile)

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(VaccineBooking)
