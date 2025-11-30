from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'vailed_from', 'vailed_to', 'discount', 'active')
    list_filter = ('active', 'vailed_from', 'vailed_to')
    search_fields = ('code',)