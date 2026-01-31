from .models import Product


def get_products_by_category(category_id):
    """
    Возвращает список опубликованных продуктов в указанной категории
    """
    return Product.objects.filter(
        category_id=category_id,
        publication_status=Product.PublicationStatus.PUBLISHED
    ).select_related('category').order_by('name')
