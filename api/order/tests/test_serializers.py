from decimal import Decimal

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from api.catalog.models import Catalog
from api.product.models import Product
from api.wishlist.models import Wishlist
from api.customer.models import Customer
from api.order.models import Order

from api.coupon.models import CouponFixedValue, CouponFirstBuy

from api.order.serializers import OrderSerializer

User = get_user_model()


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        # USER + CATALOG (auto)
        self.user = User.objects.create_user(
            username="daniel",
            email="daniel@test.com",
            password="123456"
        )

        self.catalog = Catalog.objects.get(user=self.user)

        # PRODUCT
        self.product = Product.objects.create(
            catalog=self.catalog,
            title="Produto teste",
            description="Desc",
            price=Decimal("100.00")
        )

        # SESSION (simulando request.session)
        self.request = self.factory.post("/")
        self.request.session = self.client.session
        self.request.session.save()

        # WISHLIST
        self.wishlist = Wishlist.objects.create(
            product=self.product,
            quantity=2,
            session_key=self.request.session.session_key
        )

        # CUPONS
        self.coupon = CouponFixedValue.objects.create(
            catalog=self.catalog,
            name="Cupom fixo",
            code="FIX10",
            discount_value=Decimal("10.00")
        )

        self.first_buy_coupon = CouponFirstBuy.objects.create(
            catalog=self.catalog,
            name="Primeira compra",
            code="FIRST20",
            percent_discount=Decimal("20.00")
        )

    def get_payload(self, coupon_code=None):
        return {
            "customer": {
                "email": "cliente@test.com",
                "first_name": "Daniel",
                "last_name": "Gomes",
                "address": {
                    "street": "Rua Teste",
                    "number": "123",
                    "neighborhood": "Centro",
                    "city": "Feira",
                    "state": "BA",
                    "zip_code": "44000000"
                }
            },
            "items": [
                {
                    "wishlist_product_id": self.wishlist.id
                }
            ],
            "payment_method": "pix",
            "coupon_code": coupon_code
        }

    def get_serializer(self, data):
        view = type("MockView", (), {"kwargs": {"catalog_pk": self.catalog.id}})
        return OrderSerializer(
            data=data,
            context={
                "request": self.request,
                "view": view
            }
        )

    def test_create_order_without_coupon(self):
        serializer = self.get_serializer(self.get_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()

        self.assertEqual(order.subtotal, Decimal("200.00"))

        self.assertEqual(order.total, Decimal("160.00"))
        self.assertIsNotNone(order.coupon)

    def test_create_order_with_fixed_coupon(self):
        serializer = self.get_serializer(
            self.get_payload(coupon_code="FIX10")
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()

        self.assertEqual(order.discount, Decimal("10.00"))
        self.assertEqual(order.total, Decimal("190.00"))

    def test_create_order_invalid_coupon(self):
        serializer = self.get_serializer(
            self.get_payload(coupon_code="INVALID")
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        with self.assertRaises(Exception):
            serializer.save()

    def test_wishlist_becomes_inactive(self):
        serializer = self.get_serializer(self.get_payload())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.wishlist.refresh_from_db()
        self.assertFalse(self.wishlist.is_active)

    def test_customer_created(self):
        serializer = self.get_serializer(self.get_payload())
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        self.assertEqual(order.customer.email, "cliente@test.com")

    def test_update_order_change_coupon(self):

        serializer = self.get_serializer(self.get_payload())
        serializer.is_valid(raise_exception=True)
        order = serializer.save()


        new_coupon = CouponFixedValue.objects.create(
            catalog=self.catalog,
            name="Novo",
            code="FIX50",
            discount_value=Decimal("50.00")
        )

        update_data = {
            "coupon_code": "FIX50",
            "customer": {
                "first_name": "Novo Nome"
            }
        }

        serializer = OrderSerializer(
            instance=order,
            data=update_data,
            partial=True,
            context={
                "request": self.request,
                "view": type("MockView", (), {"kwargs": {"catalog_pk": self.catalog.id}})
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()

        order.refresh_from_db()
        order.customer.refresh_from_db()

        self.assertEqual(order.coupon.id, new_coupon.id)
        self.assertEqual(order.customer.first_name, "Novo Nome")