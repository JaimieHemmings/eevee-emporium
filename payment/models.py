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
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.EmailField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_county = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default='United Kingdom'
    )

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"Shipping Address - {str(self.id)}"
    

@receiver(post_save, sender=User)
def create_shipping_address(sender, instance, created, **kwargs):
    """
    Signal to create a ShippingAddress instance when a User is created.
    """
    if created:
        shipping_address = ShippingAddress(user=instance)
        shipping_address.save()
