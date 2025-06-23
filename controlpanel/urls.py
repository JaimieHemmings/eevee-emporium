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
    )
]
