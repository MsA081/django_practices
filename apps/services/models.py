from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("عنوان"))
    slug = models.SlugField(unique=True, allow_unicode=True, help_text=_("برای سئو (SEO)"))
    # 🌟 Self-referential ForeignKey: برای ساخت زیرمجموعه‌های تو در تو (مادر/فرزند)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, 
        related_name='children', verbose_name=_("دسته مادر")
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("دسته‌بندی")
        verbose_name_plural = _("دسته‌بندی‌ها")
        unique_together = ('parent', 'name') # جلوگیری از نام تکراری در یک سطح

    def __str__(self):
        # نمایش سلسله‌مراتب: نظافت > نظافت راه پله
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField()
    # 🌟 DecimalField: حیاتی برای مسائل مالی (جلوگیری از خطای گرد کردن اعداد)
    base_price = models.DecimalField(
        max_digits=12, decimal_places=0, 
        validators=[MinValueValidator(0)], verbose_name=_("قیمت پایه (تومان)")
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 🌟 Indexing: سرعت جستجو را ۱۰۰ برابر می‌کند
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['base_price']),
        ]
        # Constraints: گارانتی در سطح دیتابیس که قیمت منفی وارد نشود
        constraints = [
            models.CheckConstraint(check=models.Q(base_price__gte=0), name='price_gte_0'),
        ]

    def __str__(self):
        return f"{self.title} - {self.base_price:,} تومان"