from django.db import models
from django.conf import settings

from api.product.models import Product

User = settings.AUTH_USER_MODEL

class Wishlist(models.Model):

	product = models.ForeignKey(
		Product,
		on_delete=models.CASCADE,
		related_name="wishlists"
	)

	quantity = models.PositiveBigIntegerField(
		default=1,
		null=False,
		blank=False
	)

	session_key = models.CharField(
		max_length=40,
		null=True,
		blank=True,
		db_index=True
	)

	is_active = models.BooleanField(
		default=True
	)

	created_at = models.DateTimeField(
		auto_now_add=True
	)

	updated_at = models.DateTimeField(
		auto_now=True
	)

	class Meta:

		verbose_name = "Wishlist"
		verbose_name_plural = "Wishlists"
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["session_key"]),
			models.Index(fields=["created_at"]),
		]
		constraints = [
			models.UniqueConstraint(
				fields=["product", "session_key"],
				name="unique_product_session_wishlist"
			),
		]

	def __str__(self):

		return f"Session {self.session_key} - {self.product}"