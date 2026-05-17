from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from api.catalog.models import Catalog
from api.product.models import Product
from api.wishlist.models import Wishlist
from api.customer.models import Customer
from api.order.models import Order, ProductOrder

from api.coupon.models import (
    CouponFixedValue,
    CouponPercentValue,
    CouponProgressive,
    CouponFirstBuy
)

User = get_user_model()


class OrderModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="daniel",
            email="daniel@test.com",
            password="123456789"
        )

        self.catalog = Catalog.objects.get(user=self.user)

        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto teste",
            description="Descrição teste",
            price=Decimal("100.00")
        )

        self.wishlist = Wishlist.objects.create(
            product=self.product,
            quantity=2,
            session_key="test-session-123"
        )

        self.customer = Customer.objects.create(
            catalog=self.catalog,
            session_key="test-session-123",
            email="customer@test.com",
            first_name="Daniel",
            last_name="Gomes",
            full_name="Daniel Gomes"
        )

        self.fixed_coupon = CouponFixedValue.objects.create(
            catalog=self.catalog,
            name="Cupom fixo",
            code="FIX10",
            discount_value=Decimal("10.00")
        )

        self.percent_coupon = CouponPercentValue.objects.create(
            catalog=self.catalog,
            name="Cupom %",
            code="PERC10",
            percent_discount=Decimal("10.00")
        )

        self.progressive_coupon = CouponProgressive.objects.create(
            catalog=self.catalog,
            name="Cupom progressivo",
            code="PROG10",
            min_purchase_value=Decimal("50.00"),
            max_purchase_value=Decimal("500.00"),
            percent_discount=Decimal("15.00")
        )

        self.first_buy_coupon = CouponFirstBuy.objects.create(
            catalog=self.catalog,
            name="Primeira compra",
            code="FIRST10",
            percent_discount=Decimal("20.00")
        )

        self.order = Order.objects.create(
            catalog=self.catalog,
            customer=self.customer
        )

        ProductOrder.objects.create(
            order=self.order,
            wishlist_product=self.wishlist
        )

    def test_order_creation(self):

        self.assertEqual(self.order.catalog, self.catalog)
        self.assertEqual(self.order.customer, self.customer)
        self.assertFalse(self.order.is_paid)

    def test_order_string_representation(self):

        self.assertIn("Pedido", str(self.order))

    def test_is_first_buy_returns_true(self):

        self.assertTrue(self.order.is_first_buy())

    def test_apply_first_buy_coupon(self):

        self.order.apply_first_buy_coupon()
        self.assertEqual(self.order.coupon, self.first_buy_coupon)

    def test_calculate_totals_without_coupon(self):

        self.order.calculate_totals()

        self.assertEqual(self.order.subtotal, Decimal("200.00"))
        self.assertEqual(self.order.total, Decimal("160.00"))

    def test_calculate_totals_fixed_coupon(self):

        self.order.coupon = self.fixed_coupon
        self.order.calculate_totals()

        self.assertEqual(self.order.subtotal, Decimal("200.00"))
        self.assertEqual(self.order.discount, Decimal("10.00"))
        self.assertEqual(self.order.total, Decimal("190.00"))

    def test_calculate_totals_percent_coupon(self):

        self.order.coupon = self.percent_coupon
        self.order.calculate_totals()

        self.assertEqual(self.order.discount, Decimal("20.00"))
        self.assertEqual(self.order.total, Decimal("180.00"))

    def test_calculate_totals_progressive_coupon(self):

        self.order.coupon = self.progressive_coupon
        self.order.calculate_totals()

        self.assertEqual(self.order.discount, Decimal("30.00"))
        self.assertEqual(self.order.total, Decimal("170.00"))