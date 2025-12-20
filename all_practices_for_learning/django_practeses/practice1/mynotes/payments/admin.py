from django.contrib import admin
from .models import Payments


# -----------------------------
# کلاس مدیریتی برای مدل Payments
# -----------------------------
class PaymentsAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست نمایش داده می‌شوند
    list_display = (
        "id",
        "status",
        "total_price_display",
        "remaining_balance_display",
        "wallet_balance_amount",
        "current_balance",
        "created_at",
    )
    list_filter = ("status", "created_at")  # فیلتر سریع بر اساس وضعیت و تاریخ
    search_fields = ("id", "status")        # امکان جست‌وجو بر اساس شناسه و وضعیت
    readonly_fields = ("created_at", "updated_at", "current_balance")  # فیلدهای سیستمی فقط خواندنی

    # نمایش مجموع قیمت (قیمت × تعداد)
    def total_price_display(self, obj):
        return f"{obj.total_price():,}"  # جداکننده هزارگان برای خوانایی بهتر
    total_price_display.short_description = "مبلغ کل"
    total_price_display.admin_order_field = "product_price"

    # نمایش موجودی باقی‌مانده
    def remaining_balance_display(self, obj):
        return f"{obj.remaining_balance():,}"
    remaining_balance_display.short_description = "موجودی پس از خرید"

    # کنترل دسترسی‌ها (اینجا فقط حذف غیرفعال شد)
    def has_delete_permission(self, request, obj=None):
        return False

    # -----------------------------
    # اکشن‌های سفارشی
    # -----------------------------
    @admin.action(description="تأیید پرداخت انتخاب‌شده‌ها")
    def mark_as_paid(self, request, queryset):
        for payment in queryset:
            if payment.is_enough_balance():
                payment.buy()

    @admin.action(description="مرجوع کردن انتخاب‌شده‌ها")
    def refund_selected(self, request, queryset):
        for payment in queryset:
            if payment.status == 'paid':
                payment.refund()

    actions = [mark_as_paid, refund_selected]


# ثبت مدل در پنل مدیریت
admin.site.register(Payments, PaymentsAdmin)
