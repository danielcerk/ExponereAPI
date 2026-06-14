from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from api.catalog.models import Catalog
from api.category.models import Category, SubCategory
from api.product.models import Product, ProductLogisticInfo, Image


User = get_user_model()


class ProductModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="123456"
        )

        self.category = Category.objects.create(
            catalog=self.user.catalog,
            name="Calças"
        )

        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Skinny"
        )

        self.product = Product.objects.create(
            catalog=self.user.catalog,
            title="Calça Jeans Skinny",
            description="Descrição teste",
            price=Decimal("129.90")
        )

    def test_create_product(self):
        self.assertEqual(self.product.title, "Calça Jeans Skinny")
        self.assertEqual(self.product.price, Decimal("129.90"))

    def test_slug_is_generated(self):
        self.assertEqual(self.product.slug, "calca-jeans-skinny")

    def test_slug_is_not_overwritten(self):
        product = Product.objects.create(
            catalog=self.user.catalog,
            title="Produto Teste",
            slug="slug-customizado",
            description="teste"
        )

        self.assertEqual(product.slug, "slug-customizado")

    def test_product_default_price(self):
        product = Product.objects.create(
            catalog=self.user.catalog,
            title="Produto sem preço",
            description="teste"
        )

        self.assertEqual(product.price, 0.01)

    def test_product_default_flags(self):
        self.assertTrue(self.product.promotion_is_active)
        self.assertTrue(self.product.is_active)

    def test_add_category(self):
        self.product.category.add(self.category)
        self.assertEqual(self.product.category.count(), 1)

    def test_add_subcategory(self):
        self.product.subcategory.add(self.subcategory)
        self.assertEqual(self.product.subcategory.count(), 1)

    def test_product_ordering_meta(self):
        self.assertEqual(Product._meta.ordering, ['-updated_at'])


class ProductLogisticInfoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="logisticuser",
            email="logistic@test.com",
            password="123456"
        )

        self.product = Product.objects.create(
            catalog=self.user.catalog,
            title="Produto Logístico",
            description="Teste"
        )

        self.logistic = ProductLogisticInfo.objects.create(
            product=self.product,
            weight=Decimal("0.500"),
            height=Decimal("10.00"),
            width=Decimal("20.00"),
            length=Decimal("30.00"),
            unit_of_measure="cm",
            packaging_type="box",
            quantity_per_box=2
        )

    def test_create_logistic_info(self):
        self.assertEqual(self.logistic.product, self.product)
        self.assertEqual(self.logistic.weight, Decimal("0.500"))

    def test_logistic_str(self):
        self.assertEqual(
            str(self.logistic),
            f"Logística de {self.product.title}"
        )

    def test_calculated_volume(self):

        self.assertEqual(
            self.logistic.calculated_volume,
            Decimal("6000.0000")
        )

    def test_calculated_volume_none(self):

        logistic = ProductLogisticInfo.objects.create(
            product=Product.objects.create(
                catalog=self.user.catalog,
                title="Outro Produto",
                description="Teste"
            )
        )

        self.assertIsNone(logistic.calculated_volume)

    def test_one_to_one_constraint(self):

        with self.assertRaises(Exception):

            ProductLogisticInfo.objects.create(
                product=self.product
            )

class ImageModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="imageuser",
            email="image@test.com",
            password="123456"
        )

        self.product = Product.objects.create(
            catalog=self.user.catalog,
            title="Produto Imagem",
            description="Teste"
        )

    def test_create_image(self):

        image = Image.objects.create(
            product=self.product,
            image="https://placehold.co/600"
        )

        self.assertEqual(image.product, self.product)
        self.assertEqual(image.image, "https://placehold.co/600")

    def test_default_image_url(self):

        image = Image.objects.create(product=self.product)

        self.assertEqual(
            image.image,
            "https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png"
        )

    def test_alt_text_is_generated(self):

        image = Image.objects.create(
            product=self.product,
            image="https://placehold.co/600"
        )

        expected = f"Foto de {self.product.title} da {self.product.catalog.name}"

        self.assertEqual(image.alt_text, expected)

    def test_custom_alt_text_is_preserved(self):

        image = Image.objects.create(
            product=self.product,
            image="https://placehold.co/600",
            alt_text="Imagem personalizada"
        )

        self.assertEqual(image.alt_text, "Imagem personalizada")

    def test_image_limit_per_product(self):

        Image.objects.create(product=self.product)
        Image.objects.create(product=self.product)
        Image.objects.create(product=self.product)

        with self.assertRaises(ValidationError):

            Image.objects.create(product=self.product)

    def test_image_str(self):

        image = Image.objects.create(product=self.product)

        self.assertIn("Imagem #", str(image))

    def test_image_ordering_meta(self):

        self.assertEqual(Image._meta.ordering, ['-created_at'])