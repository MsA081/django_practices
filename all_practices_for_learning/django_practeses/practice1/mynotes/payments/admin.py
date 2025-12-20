from django.contrib import admin
from .models import Payments


class PaymentsAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست نمایش داده می‌شوند
    list_display = ("id", "status", "total_price_display", "wallet_balance_amount", "current_balance", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "status")
    readonly_fields = ("created_at", "updated_at", "current_balance")

    # نمایش مجموع قیمت (قیمت × تعداد)
    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "مبلغ کل"
    total_price_display.admin_order_field = "product_price"

    # نمایش موجودی باقی‌مانده
    def remaining_balance_display(self, obj):
        return obj.remaining_balance()
    remaining_balance_display.short_description = "موجودی پس از خرید"

    # کنترل دسترسی‌ها (اینجا فقط حذف رو غیرفعال کردیم)
    def has_delete_permission(self, request, obj=None):
        return False


# ثبت مدل در پنل مدیریت
admin.site.register(Payments, PaymentsAdmin)
