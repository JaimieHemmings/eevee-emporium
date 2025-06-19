from django.db import models
import datetime
from django.utils.text import slugify


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
