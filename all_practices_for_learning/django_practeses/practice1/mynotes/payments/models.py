from django.db import models
from django.utils import timezone


class Payments(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
        ('refunded', 'مرجوع شده'),
    )

    product_price = models.PositiveIntegerField(verbose_name="قیمت محصول")
    quantity = models.PositiveIntegerField(verbose_name="تعداد", default=1)

    wallet_balance_amount = models.PositiveIntegerField(verbose_name="موجودی کیف پول")
    current_balance = models.PositiveIntegerField(verbose_name="موجودی فعلی", default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت پرداخت"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # محاسبات
    # -----------------------------
    def total_price(self):
        return self.product_price * self.quantity

    def remaining_balance(self):
        return self.wallet_balance_amount - self.total_price()

    def is_enough_balance(self):
        return self.remaining_balance() >= 0

    # -----------------------------
    # عملیات پرداخت
    # -----------------------------
    def update_balance(self):
        self.wallet_balance_amount = self.remaining_balance()
        self.current_balance = self.wallet_balance_amount
        self.save()
        return self.wallet_balance_amount

    def buy(self):
        if self.is_enough_balance():
            self.update_balance()
            self.status = 'paid'
            self.save()
            return True
        self.status = 'failed'
        self.save()
        return False

    def refund(self):
        self.wallet_balance_amount += self.total_price()
        self.current_balance = self.wallet_balance_amount
        self.status = 'refunded'
        self.save()
        return self.wallet_balance_amount

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"
