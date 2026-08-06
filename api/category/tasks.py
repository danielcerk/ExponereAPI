from celery import shared_task

from django.utils.text import slugify

from api.catalog.models import Catalog
from api.category.models import Category, SubCategory

CATEGORIES = {
    "Moda": {
        "Feminino": [
            "Vestidos",
            "Blusas",
            "Calças",
            "Saias",
            "Shorts",
            "Conjuntos",
            "Moda íntima",
            "Moda praia",
        ],
        "Masculino": [
            "Camisetas",
            "Camisas",
            "Calças",
            "Bermudas",
            "Jaquetas",
            "Moda íntima",
        ],
        "Infantil": [
            "Meninas",
            "Meninos",
            "Bebês",
        ],
    },

    "Calçados": {
        "Feminino": [
            "Tênis",
            "Sandálias",
            "Scarpins",
            "Botas",
            "Rasteiras",
            "Chinelos",
        ],
        "Masculino": [
            "Tênis",
            "Sapatos",
            "Botas",
            "Sandálias",
            "Chinelos",
        ],
        "Infantil": [
            "Tênis",
            "Sandálias",
            "Botas",
        ],
    },

    "Bolsas e Acessórios": {
        "Bolsas": [
            "Mochilas",
            "Bolsas de mão",
            "Bolsas transversais",
            "Carteiras",
        ],
        "Acessórios": [
            "Bonés",
            "Cintos",
            "Óculos",
            "Relógios",
            "Lenços",
        ],
    },

    "Joias e Bijuterias": {
        "Joias": [
            "Anéis",
            "Brincos",
            "Pulseiras",
            "Colares",
            "Pingentes",
        ],
        "Bijuterias": [
            "Anéis",
            "Brincos",
            "Pulseiras",
            "Colares",
        ],
    },

    "Beleza": {
        "Maquiagem": [
            "Bases",
            "Batom",
            "Máscara",
            "Paletas",
        ],
        "Cabelos": [
            "Shampoo",
            "Condicionador",
            "Máscaras",
            "Finalizadores",
        ],
        "Perfumes": [
            "Femininos",
            "Masculinos",
            "Infantis",
        ],
        "Skincare": [
            "Sabonetes",
            "Hidratantes",
            "Séruns",
            "Protetor solar",
        ],
    },

    "Saúde": {
        "Suplementos": [
            "Vitaminas",
            "Proteínas",
            "Creatina",
        ],
        "Cuidados": [
            "Primeiros socorros",
            "Ortopedia",
            "Higiene",
        ],
    },

    "Alimentos e Bebidas": {
        "Alimentos": [
            "Doces",
            "Salgados",
            "Congelados",
            "Naturais",
        ],
        "Bebidas": [
            "Refrigerantes",
            "Sucos",
            "Água",
            "Energéticos",
        ],
    },

    "Casa e Decoração": {
        "Decoração": [
            "Quadros",
            "Espelhos",
            "Vasos",
            "Tapetes",
        ],
        "Utilidades": [
            "Cozinha",
            "Banheiro",
            "Organização",
        ],
    },

    "Móveis": {
        "Sala": [
            "Sofás",
            "Mesas",
            "Painéis",
        ],
        "Quarto": [
            "Camas",
            "Guarda-roupas",
            "Criados-mudos",
        ],
        "Escritório": [
            "Mesas",
            "Cadeiras",
        ],
    },

    "Construção e Ferramentas": {
        "Ferramentas": [
            "Elétricas",
            "Manuais",
        ],
        "Materiais": [
            "Tintas",
            "Cimento",
            "Hidráulica",
            "Elétrica",
        ],
    },

    "Eletrodomésticos": {
        "Cozinha": [
            "Geladeiras",
            "Fogões",
            "Micro-ondas",
        ],
        "Lavanderia": [
            "Máquinas",
            "Secadoras",
        ],
    },

    "Eletrônicos": {
        "TV e Áudio": [
            "Smart TVs",
            "Caixas de som",
            "Fones",
        ],
        "Celulares": [
            "Smartphones",
            "Tablets",
            "Smartwatch",
        ],
    },

    "Informática": {
        "Computadores": [
            "Notebooks",
            "Desktops",
        ],
        "Periféricos": [
            "Teclados",
            "Mouses",
            "Monitores",
            "Impressoras",
        ],
    },

    "Games": {
        "Consoles": [
            "PlayStation",
            "Xbox",
            "Nintendo",
        ],
        "Jogos": [
            "Mídia física",
            "Digital",
        ],
        "Acessórios": [
            "Controles",
            "Headsets",
        ],
    },

    "Automotivo": {
        "Peças": [
            "Motor",
            "Suspensão",
            "Freios",
        ],
        "Acessórios": [
            "Capas",
            "Som",
            "Iluminação",
        ],
    },

    "Esportes e Lazer": {
        "Academia": [
            "Roupas",
            "Equipamentos",
        ],
        "Futebol": [
            "Bolas",
            "Chuteiras",
        ],
        "Camping": [
            "Barracas",
            "Mochilas",
        ],
    },

    "Pet Shop": {
        "Cães": [
            "Ração",
            "Brinquedos",
            "Coleiras",
        ],
        "Gatos": [
            "Ração",
            "Areia",
            "Brinquedos",
        ],
    },

    "Brinquedos": {
        "Educativos": [],
        "Bonecas": [],
        "Carrinhos": [],
        "Jogos": [],
    },

    "Papelaria e Livros": {
        "Papelaria": [
            "Cadernos",
            "Canetas",
            "Mochilas",
        ],
        "Livros": [
            "Infantis",
            "Romance",
            "Negócios",
        ],
    },

    "Bebês": {
        "Roupas": [],
        "Higiene": [],
        "Alimentação": [],
        "Brinquedos": [],
    },

    "Música": {
        "Instrumentos": [
            "Violão",
            "Guitarra",
            "Teclado",
            "Bateria",
        ],
        "Acessórios": [
            "Cordas",
            "Capotraste",
            "Cases",
        ],
    },

    "Festas e Presentes": {
        "Decoração": [],
        "Lembrancinhas": [],
        "Presentes": [],
    },

    "Artesanato": {
        "Materiais": [],
        "Produtos artesanais": [],
    },

    "Agro e Jardinagem": {
        "Jardinagem": [
            "Vasos",
            "Ferramentas",
            "Sementes",
        ],
        "Agro": [
            "Insumos",
            "Equipamentos",
        ],
    },

    "Serviços": {
        "Consultoria": [],
        "Assistência técnica": [],
        "Design": [],
        "Marketing": [],
        "Outros": [],
    },

    "Outros": {
        "Geral": [],
    },
}

@shared_task
def generate_categories(catalog_id):

    catalog = Catalog.objects.select_related(
        "business_category"
    ).get(id=catalog_id)

    if not catalog.business_category:

        return

    data = CATEGORIES.get(catalog.business_category.name)

    if not data:

        return

    for category_name, subcategories in data.items():

        category, _ = Category.objects.get_or_create(
            catalog=catalog,
            name=category_name,
            defaults={
                "slug": slugify(category_name),
            },
        )

        for subcategory_name in subcategories:
            SubCategory.objects.get_or_create(
                category=category,
                name=subcategory_name,
                defaults={
                    "slug": slugify(subcategory_name),
                },
            )