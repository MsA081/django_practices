from django.db import models
from django.db.models import Avg, Q, F, Count


class ProductManager(models.Manager):

    # ✅ محصولات گران‌تر از میانگین قیمت
    def expensive(self):
        avg_price = self.aggregate(Avg("price"))["price__avg"]
        return self.filter(price__gt=avg_price)

    # ✅ محصولاتی که موجودی آن‌ها کمتر از ۵ است
    def low_stock(self, threshold=5):
        return self.filter(stock__lt=threshold)

    # ✅ جستجو در نام محصول
    def search(self, text):
        return self.filter(name__icontains=text)

    # ✅ محصولات فعال با بازهٔ قیمت
    def active_in_range(self, min_price, max_price):
        return self.filter(
            is_active=True,
            price__gte=min_price,
            price__lte=max_price
        )

    # ✅ محصولات یک دسته‌بندی خاص
    def by_category(self, category_name):
        return self.filter(category__name__iexact=category_name)

    # ✅ محصولات با شرط‌های پیچیده (OR)
    def complex_filter(self):
        return self.filter(
            Q(stock__lt=5) | Q(price__gt=10_000_000)
        )

    # ✅ مقایسهٔ فیلدها با F
    def wrong_stock(self):
        return self.filter(quantity__gt=F("stock"))

    # ✅ افزودن فیلد محاسباتی total_price
    def with_total_price(self):
        return self.annotate(total=F("price") * F("quantity"))

    # ✅ گزارش‌گیری: بیشترین، کمترین، میانگین قیمت
    def price_stats(self):
        return self.aggregate(
            max_price=models.Max("price"),
            min_price=models.Min("price"),
            avg_price=models.Avg("price")
        )

    # ✅ تعداد محصولات هر دسته‌بندی
    def category_stats(self):
        return self.values("category__name").annotate(
            total_products=Count("id")
        )
