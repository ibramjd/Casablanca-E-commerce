from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone_number')
    search_fields = ('name', 'email')
    list_filter = ('user',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'type_of_clothe')
    search_fields = ('name', 'category')
    list_filter = ('category',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')
    search_fields = ('customer__name', 'transaction_id')
    list_filter = ('complete', 'date_ordered')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'get_total', 'date_added')
    search_fields = ('order__transaction_id', 'product__name')
    list_filter = ('order__date_ordered',)

    def get_total(self, obj):
        return obj.quantity * obj.product.price
    get_total.short_description = 'Total'

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'state', 'street', 'phone_number', 'date_added')
    search_fields = ('customer__name', 'order__transaction_id', 'address')
    list_filter = ('date_added',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'get_state', 'transaction_id', 'amount', 'date_paid')
    search_fields = ('transaction_id', 'customer__name')
    list_filter = ('date_paid',)

    def get_state(self, obj):
        address = ShippingAddress.objects.filter(order=obj.order).last()
        return address.state if address else "-"
    get_state.short_description = 'State'

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)