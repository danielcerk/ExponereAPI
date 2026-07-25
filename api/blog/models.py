from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Post(models.Model):

    title = models.CharField(
        verbose_name="Título",
        max_length=255,
    )

    subtitle = models.CharField(
        verbose_name="Subtítulo",
        max_length=255,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        verbose_name="Slug",
        max_length=255,
        unique=True,
        blank=True,
    )

    image = models.URLField(
        verbose_name="Imagem de capa",
        max_length=500,
        blank=True,
        default="https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png",
        help_text="Cole a URL da imagem de capa do post.",
    )

    content = models.TextField(
        verbose_name="Conteúdo",
        help_text="Conteúdo principal do artigo.",
    )

    author = models.CharField(
        verbose_name="Autor",
        max_length=150,
        blank=True,
        default="Produtos Nordeste",
    )

    is_published = models.BooleanField(
        verbose_name="Publicado",
        default=False,
        help_text="Define se o post está visível no blog.",
    )

    published_at = models.DateTimeField(
        verbose_name="Publicado em",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["published_at"]),
        ]

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)

        if self.is_published and not self.published_at:

            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title