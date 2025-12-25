from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными для категорий и товаров"

    def handle(self, *args, **options):
        # Удаление существующих данных
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()

        if deleted_products or deleted_categories:
            self.stdout.write(
                self.style.WARNING(
                    f"Удалено {deleted_products} товаров и {deleted_categories} категорий"
                )
            )

        # Создание категорий
        categories = [
            {"name": "Электроника", "description": "Техника и гаджеты"},
            {"name": "Одежда", "description": "Мужская и женская одежда"},
            {"name": "Книги", "description": "Художественная и учебная литература"},
            {"name": "Спорт", "description": "Спортивные товары и инвентарь"},
            {"name": "Дом и сад", "description": "Товары для дома и сада"},
        ]

        created_categories = {}
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"], defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Создана категория: {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Категория уже существует: {category.name}")
                )
            created_categories[cat_data["name"]] = category

        # Создание товаров
        products = [
            {
                "name": "Смартфон",
                "description": "Мощный смартфон с отличной камерой",
                "price": 499.99,
                "category": "Электроника",
            },
            {
                "name": "Ноутбук",
                "description": "Производительный ноутбук для работы и развлечений",
                "price": 1299.99,
                "category": "Электроника",
            },
            {
                "name": "Футболка",
                "description": "Хлопковая футболка",
                "price": 29.99,
                "category": "Одежда",
            },
            {
                "name": "Джинсы",
                "description": "Классические джинсы",
                "price": 89.99,
                "category": "Одежда",
            },
            {
                "name": "1984",
                "description": "Роман-антиутопия Джорджа Оруэлла",
                "price": 15.50,
                "category": "Книги",
            },
            {
                "name": "Мяч футбольный",
                "description": "Официальный матчевый мяч",
                "price": 59.99,
                "category": "Спорт",
            },
            {
                "name": "Горшок для цветов",
                "description": "Керамический горшок для комнатных растений",
                "price": 24.99,
                "category": "Дом и сад",
            },
        ]

        created_count = 0
        for prod_data in products:
            category_name = prod_data.pop("category")
            category = created_categories[category_name]

            product, created = Product.objects.get_or_create(
                name=prod_data["name"], defaults={**prod_data, "category": category}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Создан товар: {product.name} ({category.name}) - {product.price} руб."
                    )
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f"Товар уже существует: {product.name}")
                )

        total_products = Product.objects.count()
        total_categories = Category.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово! Всего категорий: {total_categories}, "
                f"товаров: {total_products} (создано: {created_count})"
            )
        )
