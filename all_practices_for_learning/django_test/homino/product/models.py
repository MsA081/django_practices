from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .managers import ProductManager


# ✅ مدل دسته‌بندی
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    # ✅ ساخت slug خودکار
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



# ✅ مدل محصول
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # ✅ اعتبارسنجی حرفه‌ای
    def clean(self):
        if self.price < 0:
            raise ValidationError("قیمت نمی‌تواند منفی باشد.")

        if self.quantity < 0:
            raise ValidationError("تعداد نمی‌تواند منفی باشد.")

        if self.stock < 0:
            raise ValidationError("موجودی نمی‌تواند منفی باشد.")

        if len(self.name) < 3:
            raise ValidationError("نام محصول باید حداقل ۳ کاراکتر باشد.")

        if not self.category:
            raise ValidationError("محصول باید دسته‌بندی داشته باشد.")

        if not self.is_active and self.stock > 0:
            raise ValidationError("محصول غیرفعال نمی‌تواند موجودی داشته باشد.")

    # ✅ اجرای clean() قبل از ذخیره
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # ✅ قیمت کل (قیمت × تعداد)
    @property
    def total_price(self):
        return self.price * self.quantity
    
    objects = ProductManager()

