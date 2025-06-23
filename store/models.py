from django.db import models
import datetime
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    """
    Profile model to extend the User model with additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='United Kingdom')
    old_cart = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

# Create a user profile automatically when a User is created
def create_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a User is created.
    """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# Connect the create_profile function to the post_save signal of User
post_save.connect(create_profile, sender=User)


# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, editable=False
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        # Handle duplicate slugs by adding a number
        original_slug = self.slug
        counter = 1
        while Product.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# Sets of products
class Set(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, editable=False
    )
    image = models.ImageField(upload_to='uploads/sets/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        # Handle duplicate slugs by adding a number
        original_slug = self.slug
        counter = 1
        while Product.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Customers who can place orders
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # Store hashed passwords in production
    password = models.CharField(max_length=128)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Products available in the store
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    set = models.ForeignKey(
        Set, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='uploads/product/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, editable=False
    )

    # Save the slug based on the product name, ensuring uniqueness
    # If the name changes, update the slug accordingly
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        else:
            # For existing objects, compare with database
            original = Product.objects.get(id=self.id)
            if original.name != self.name:
                # Only update slug if name has changed
                self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Orders placed by customers
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    order_date = models.DateTimeField(default=datetime.datetime.now)
    # e.g., Pending, Shipped, Delivered
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} by "
    "{self.customer.first_name} {self.customer.last_name}"
