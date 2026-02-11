from django.db.models import F, Q, Sum

# ۱. افزایش قیمت ۱۰ درصدی برای تمام خدمات نظافت (Bulk Update)
# استفاده از F() برای اشاره به مقدار فعلی فیلد در دیتابیس
Service.objects.filter(category__name__contains='نظافت').update(base_price=F('base_price') * 1.1)

# ۲. پیدا کردن سرویس‌های ارزان (زیر ۵۰۰ تومان) یا سرویس‌های ویژه (جستجوی ترکیبی)
cheap_or_special = Service.objects.filter(
    Q(base_price__lt=500000) | Q(description__contains='ویژه')
)

# ۳. گزارش مالی: مجموع درآمد از سفارش‌های تکمیل شده
total_revenue = Order.objects.filter(status='completed').aggregate(
    revenue=Sum(F('items__price_at_order') * F('items__quantity'))
)