from django.contrib import admin
from .models import Category, Customer, Product, Order, Set, Profile
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Set)
admin.site.register(Profile)

# Mix profile and user information
class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    field = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    inlines = [ProfileInline]

# Register the User model with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
