from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id):
    """
    Возвращает список опубликованных продуктов в указанной категории с низкоуровневым кэшированием
    """
    cache_key = f'category_products_{category_id}'
    cached_products = cache.get(cache_key)
    
    if cached_products is None:
        products = list(Product.objects.filter(
            category_id=category_id,
            publication_status=Product.PublicationStatus.PUBLISHED
        ).select_related('category').order_by('name'))
        
        cache.set(cache_key, products, 60 * 30)  # Кэш на 30 минут
        return products
    
    return cached_products


def get_all_published_products():
    """
    Возвращает список всех опубликованных продуктов с низкоуровневым кэшированием
    """
    cache_key = 'all_published_products'
    cached_products = cache.get(cache_key)
    
    if cached_products is None:
        products = list(Product.objects.filter(
            publication_status=Product.PublicationStatus.PUBLISHED
        ).select_related('category').order_by('name'))
        
        cache.set(cache_key, products, 60 * 30)  # Кэш на 30 минут
        return products
    
    return cached_products


def clear_all_products_cache():
    """
    Очищает кэш всех опубликованных продуктов
    """
    cache_key = 'all_published_products'
    cache.delete(cache_key)


def clear_category_products_cache(category_id):
    """
    Очищает кэш продуктов для указанной категории
    """
    cache_key = f'category_products_{category_id}'
    cache.delete(cache_key)
