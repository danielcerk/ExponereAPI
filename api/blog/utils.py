from django.conf import settings
import requests
from typing import List, Dict, Optional

from rest_framework.exceptions import NotFound

API_KEY = settings.STRAPI_API_KEY
API_URL = settings.STRAPI_ARTICLE_URL

def _make_request(url: str) -> Dict:
    
    try:
        
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            timeout=50
        )

        response.raise_for_status()

        return response.json()
    
    except requests.exceptions.RequestException as e:
        
        return {"error": str(e)}


def _format_article(article: Dict) -> Dict:
    cover = article.get("cover")

    return {
        "id": article.get("id"),
        "document_id": article.get("documentId"),
        "title": article.get("title"),
        "description": article.get("description"),
        "slug": article.get("slug"),
        "created_at": article.get("createdAt"),
        "updated_at": article.get("updatedAt"),
        "published_at": article.get("publishedAt"),

        "cover": {
            "id": cover.get("id"),
            "name": cover.get("name"),
            "url": cover.get("url"),
            "width": cover.get("width"),
            "height": cover.get("height"),
        } if cover else None,

        "author": article.get("author"),

        "category": article.get("category"),

        "blocks": [
            {
                "component": block.get("__component"),
                "body": block.get("body")
            }
            for block in article.get("blocks", [])
        ]
    }

def get_all_articles(
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 25
) -> Dict:

    url = f"{API_URL}?pagination[page]={page}&pagination[pageSize]={page_size}"

    if sort:
        
        url += f"&sort[0]={sort}"

    data = _make_request(url)

    if "error" in data:
        
        return data

    articles = [_format_article(item) for item in data.get("data", [])]

    return {
        
        "articles": articles,
        "pagination": data.get("meta", {}).get("pagination", {})

    }


def get_article_by_slug(slug: str) -> Dict:

    url = f"{API_URL}?filters[slug][$eq]={slug}&populate=*"

    data = _make_request(url)

    print(data)

    if "error" in data:
        
        return data

    articles = data.get("data", [])

    if not articles:
        
        raise NotFound("Article not found")

    return _format_article(articles[0])