from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.control_panel_home,
        name='control_panel_home'
    ),
    path(
        'orders/',
        views.orders,
        name='control_panel_orders'
    ),
    path(
        'orders/<int:order_id>/',
        views.order_detail,
        name='control_panel_order_detail'
    ),
    path(
        'orders/mark_shipped/<int:order_id>/',
        views.mark_order_shipped,
        name='control_panel_mark_order_shipped'
    ),
    path(
        'products/',
        views.products,
        name='control_panel_products'
    ),
    path(
        'products/add/',
        views.add_product,
        name='control_panel_add_product'
    ),
    path(
        'edit_product/<int:product_id>/',
        views.edit_product,
        name='control_panel_edit_product'
    ),
    path(
        'delete_product/<int:product_id>/',
        views.confirm_delete_product,
        name='confirm_delete_product'
    ),
]
