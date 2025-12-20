from django.test import TestCase
from django.urls import reverse
from .models import Product, Category


class ProductTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Mobile")

    def test_create_product(self):
        product = Product.objects.create(
            name="iPhone 15",
            description="New Apple phone",
            price=50000000,
            quantity=2,
            stock=10,
            category=self.category,
            is_active=True
        )
        self.assertEqual(product.name, "iPhone 15")
        self.assertEqual(product.total_price, 100000000)

    def test_negative_price_validation(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Bad Product",
                description="Invalid",
                price=-1000,
                quantity=1,
                stock=5,
                category=self.category,
                is_active=True
            )

    def test_product_list_view(self):
        Product.objects.create(
            name="Samsung S24",
            description="Flagship",
            price=40000000,
            quantity=1,
            stock=5,
            category=self.category,
            is_active=True
        )
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Samsung S24")

    def test_delete_product(self):
        product = Product.objects.create(
            name="Test Delete",
            description="To be deleted",
            price=1000,
            quantity=1,
            stock=1,
            category=self.category,
            is_active=True
        )
        delete_url = reverse("product_delete", args=[product.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_update_product(self):
        product = Product.objects.create(
            name="Old Name",
            description="Test",
            price=1000,
            quantity=1,
            stock=1,
            category=self.category,
            is_active=True
        )
        update_url = reverse("product_update", args=[product.pk])
        response = self.client.post(update_url, {
            "name": "New Name",
            "description": "Updated",
            "price": 2000,
            "quantity": 2,
            "stock": 3,
            "category": self.category.id,
            "is_active": True
        })
        product.refresh_from_db()
        self.assertEqual(product.name, "New Name")
        self.assertEqual(product.price, 2000)
