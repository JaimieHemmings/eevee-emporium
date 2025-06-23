from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create order item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend the order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

# Register the order model with the admin
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
