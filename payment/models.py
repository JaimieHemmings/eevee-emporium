from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=5000)
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Order - {str(self.id)}"
    

@receiver(pre_save, sender=Order)
def set_date_shipped(sender, instance, **kwargs):
    """
    Signal to set the date_shipped field to the current date and time
    when the order is marked as shipped.
    """
    if instance.shipped and not instance.date_shipped:
        instance.date_shipped = datetime.datetime.now()
    elif not instance.shipped:
        instance.date_shipped = None


class OrderItem(models.Model):   
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Order Item - {str(self.id)}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    shipping_full_name = models.CharField(
        max_length=100,
        help_text="Full name for delivery"
    )
    shipping_email = models.EmailField(
        max_length=254,
        help_text="Email for delivery notifications"
    )
    shipping_address1 = models.CharField(
        max_length=255,
        verbose_name="Address Line 1",
        help_text="Street address, P.O. box, or company name"
    )
    shipping_address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Address Line 2",
        help_text="Apartment, suite, unit, building, floor, etc. (optional)"
    )
    shipping_city = models.CharField(
        max_length=50,
        help_text="City or town"
    )
    shipping_county = models.CharField(
        max_length=50,
        verbose_name="County/State",
        help_text="County, state, or region"
    )
    shipping_postcode = models.CharField(
        max_length=12,
        verbose_name="Postal Code",
        help_text="Postal code or ZIP code"
    )
    shipping_country = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default='United Kingdom',
        verbose_name="Country",
        help_text="Country name"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        help_text="Contact number for delivery (optional)"
    )
    delivery_instructions = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Delivery Instructions",
        help_text="Special delivery instructions (optional, max 500 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Shipping Addresses"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'updated_at']),
        ]

    def __str__(self):
        return f"{self.shipping_full_name} - {self.shipping_city}, {self.get_country_display()}"
    
    def get_country_display(self):
        """Return the country name (already stored as full name)"""
        return self.shipping_country
    
    def get_full_address(self):
        """Return the complete formatted address"""
        address_parts = [
            self.shipping_address1,
            self.shipping_address2,
            self.shipping_city,
            self.shipping_county,
            self.shipping_postcode,
            self.get_country_display()
        ]
        # Filter out empty parts
        return ', '.join(part for part in address_parts if part)
    

@receiver(post_save, sender=User)
def create_shipping_address(sender, instance, created, **kwargs):
    """
    Signal to create a ShippingAddress instance when a User is created.
    Only creates if the user doesn't already have a shipping address.
    """
    if created:
        # Check if user already has a shipping address to prevent duplicates
        if not ShippingAddress.objects.filter(user=instance).exists():
            shipping_address = ShippingAddress(user=instance)
            shipping_address.save()
