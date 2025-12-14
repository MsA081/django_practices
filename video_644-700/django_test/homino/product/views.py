from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Product


# ✅ لیست محصولات
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10  # صفحه‌بندی حرفه‌ای


# ✅ جزئیات محصول
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


# ✅ ایجاد محصول جدید
class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price", "image", "quantity", "category", "stock", "is_active"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")


# ✅ ویرایش محصول
class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price", "image", "quantity", "category", "stock", "is_active"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")


# ✅ حذف محصول
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
