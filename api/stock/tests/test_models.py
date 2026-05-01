from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from api.product.models import Product
from api.stock.models import (
    Stock,
    StockMovement,
    AlertProductStock,
)

User = get_user_model()


class StockModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="stockuser",
            email="stock@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto teste",
            description="Descrição"
        )

        self.stock = Stock.objects.create(
            product=self.product,
            quantity=10,
            reserved_quantity=2,
            min_quantity=1
        )

    def test_create_stock(self):
        self.assertEqual(self.stock.quantity, 10)
        self.assertEqual(self.stock.reserved_quantity, 2)
        self.assertTrue(self.stock.is_active)

    def test_available_quantity(self):
        self.assertEqual(self.stock.available_quantity, 8)

    def test_clean_reserved_greater_than_quantity(self):
        stock = Stock(
            product=self.product,
            quantity=5,
            reserved_quantity=10
        )

        with self.assertRaises(ValidationError):
            stock.full_clean()

    def test_clean_quantity_greater_than_max(self):
        stock = Stock(
            product=self.product,
            quantity=20,
            max_quantity=10
        )

        with self.assertRaises(ValidationError):
            stock.full_clean()

    def test_add_stock(self):
        self.stock.add(5)
        self.stock.refresh_from_db()

        self.assertEqual(self.stock.quantity, 15)

    def test_add_negative_amount(self):
        with self.assertRaises(ValidationError):
            self.stock.add(-1)

    def test_remove_stock(self):
        self.stock.remove(3)
        self.stock.refresh_from_db()

        self.assertEqual(self.stock.quantity, 7)

    def test_remove_insufficient_stock(self):
        with self.assertRaises(ValidationError):
            self.stock.remove(20)

    def test_reserve_stock(self):
        self.stock.reserve(3)
        self.stock.refresh_from_db()

        self.assertEqual(self.stock.reserved_quantity, 5)

    def test_reserve_insufficient_stock(self):
        with self.assertRaises(ValidationError):
            self.stock.reserve(20)

    def test_release_stock(self):
        self.stock.release(1)
        self.stock.refresh_from_db()

        self.assertEqual(self.stock.reserved_quantity, 1)

    def test_release_more_than_reserved(self):
        with self.assertRaises(ValidationError):
            self.stock.release(10)

    def test_stock_str(self):
        self.assertIn("disponíveis", str(self.stock))


class StockMovementModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="movementuser",
            email="movement@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto",
            description="Descrição"
        )

        self.stock = Stock.objects.create(
            product=self.product,
            quantity=10,
            reserved_quantity=0
        )

    def test_stock_movement_in(self):
        StockMovement.objects.create(
            stock=self.stock,
            type=StockMovement.IN,
            quantity=5
        )

        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 15)

    def test_stock_movement_out(self):
        StockMovement.objects.create(
            stock=self.stock,
            type=StockMovement.OUT,
            quantity=4
        )

        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 6)

    def test_stock_movement_reserve(self):
        StockMovement.objects.create(
            stock=self.stock,
            type=StockMovement.RESERVE,
            quantity=3
        )

        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved_quantity, 3)

    def test_stock_movement_release(self):
        self.stock.reserve(5)

        StockMovement.objects.create(
            stock=self.stock,
            type=StockMovement.RELEASE,
            quantity=2
        )

        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved_quantity, 3)

    def test_stock_movement_invalid_quantity(self):
        movement = StockMovement(
            stock=self.stock,
            type=StockMovement.IN,
            quantity=0
        )

        with self.assertRaises(ValidationError):
            movement.full_clean()

    def test_stock_movement_str(self):
        movement = StockMovement.objects.create(
            stock=self.stock,
            type=StockMovement.IN,
            quantity=2
        )

        self.assertIn("IN", str(movement))


class AlertProductStockModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="alertuser",
            email="alert@test.com",
            password="123456"
        )

        self.catalog = self.user.catalog

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto alerta",
            description="Descrição"
        )

    def test_create_alert(self):
        alert = AlertProductStock.objects.create(
            email="client@test.com",
            product=self.product
        )

        self.assertTrue(alert.is_active)
        self.assertFalse(alert.notified)

    def test_unique_email_product_constraint(self):
        AlertProductStock.objects.create(
            email="client@test.com",
            product=self.product
        )

        with self.assertRaises(ValidationError) as context:
            AlertProductStock.objects.create(
                email="client@test.com",
                product=self.product
            )

        self.assertIn(
            "já existe",
            str(context.exception)
        )

    def test_deactivate_alert(self):
        alert = AlertProductStock.objects.create(
            email="client@test.com",
            product=self.product
        )

        alert.deactivate()
        alert.refresh_from_db()

        self.assertFalse(alert.is_active)

    def test_mark_as_notified(self):
        alert = AlertProductStock.objects.create(
            email="client@test.com",
            product=self.product
        )

        alert.mark_as_notified()
        alert.refresh_from_db()

        self.assertTrue(alert.notified)

    def test_is_pending(self):
        alert = AlertProductStock.objects.create(
            email="client@test.com",
            product=self.product
        )

        self.assertTrue(alert.is_pending)

        alert.mark_as_notified()
        alert.refresh_from_db()

        self.assertFalse(alert.is_pending)

    def test_invalid_email(self):
        alert = AlertProductStock(
            email="invalid-email",
            product=self.product
        )

        with self.assertRaises(ValidationError):
            alert.full_clean()