from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ["product", "price", "quantity"]

    def has_add_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_key",
        "full_name",
        "total_paid",
        "user",
        "billing_status",
    ]
    readonly_fields = [
        "user",
        "full_name",
        "address1",
        "address2",
        "city",
        "phone",
        "postal_code",
        "total_paid",
        "order_key",
        "billing_status",
        "cardno",
        "email",
        "country_code",
        "payment_option",
        "delivery_method"
    ]
    list_filter = ["billing_status", "updated", "order_shipped"]
    inlines = [OrderItemInline]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)
