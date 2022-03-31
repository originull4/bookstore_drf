from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):
    model = Account
    add_form = AccountCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Additional Fields',{'fields':('gender', 'avatar')})
    )


admin.site.register(Account, AccountAdmin)
