from django.contrib import admin

from .models import Customer

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ["user_permissions", "last_login", "groups"]


admin.site.register(Customer, CustomerAdmin)
