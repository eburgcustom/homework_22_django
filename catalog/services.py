from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id):
    """
    Возвращает список опубликованных продуктов в указанной категории с низкоуровневым кэшированием
    """
    cache_key = f'category_products_{category_id}'
    cached_products = cache.get(cache_key)
    
    print(f"Cache key: {cache_key}")
    print(f"Cached products: {cached_products}")
    
    if cached_products is None:
        products = list(Product.objects.filter(
            category_id=category_id,
            publication_status=Product.PublicationStatus.PUBLISHED
        ).select_related('category').order_by('name'))
        
        print(f"DB query result: {products}")
        cache.set(cache_key, products, 60 * 30)  # Кэш на 30 минут
        return products
    
    return cached_products


def clear_category_products_cache(category_id):
    """
    Очищает кэш продуктов для указанной категории
    """
    cache_key = f'category_products_{category_id}'
    cache.delete(cache_key)
