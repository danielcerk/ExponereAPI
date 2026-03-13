from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from api.catalog.models import Catalog
from api.address.models import Address
from .models import Keyword


def build_keywords(catalog, address):

    keywords = set()

    name = (catalog.name or '').lower()
    category = (
        catalog.business_category.name.lower()
        if catalog.business_category else ''
    )

    city = address.city.name.lower() if address.city else ''
    state = address.state.name.lower() if address.state else ''
    neighborhood = (address.neighborhood or '').lower()

    base_terms = [
        name,
        category,
        city,
        state,
        neighborhood,
    ]

    base_terms = [term for term in base_terms if term]

    keywords.update(base_terms)

    if name and city:

        keywords.add(f'{name} {city}')

    if name and neighborhood:

        keywords.add(f'{name} {neighborhood}')

    if category and city:

        keywords.add(f'{category} em {city}')

    if category and neighborhood:

        keywords.add(f'{category} no {neighborhood}')

    if category and state:
        keywords.add(f'{category} {state}')

    if category and city:

        keywords.add(f'melhor {category} em {city}')
        keywords.add(f'{category} delivery {city}')
        keywords.add(f'{category} perto de mim')

    if name and category:

        keywords.add(f'{name} {category}')

    return keywords


@receiver(post_save, sender=Address)
def generate_catalog_keywords(sender, instance, created, **kwargs):

    catalog = Catalog.objects.filter(user=instance.user).first()

    if not catalog:

        return

    if not catalog.name:

        return

    keywords = build_keywords(catalog, instance)

    for word in keywords:

        Keyword.objects.get_or_create(
            catalog=catalog,
            keyword=word.strip().lower(),
            defaults={
                'slug': slugify(word)
            }
        )