from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными для категорий и товаров"

    def handle(self, *args, **options):
        # Удаление существующих данных
        self.stdout.write(self.style.WARNING("Удаление существующих данных..."))
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка данных из фикстур
        self._load_fixtures()

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))

    def _load_fixtures(self):
        """Загрузка данных из фикстур"""
        fixtures = [
            "catalog/fixtures/category_fixture.json",
            "catalog/fixtures/product_fixture.json",
        ]

        for fixture in fixtures:
            try:
                call_command("loaddata", fixture)
                self.stdout.write(self.style.SUCCESS(f"Успешно загружено: {fixture}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка при загрузке {fixture}: {str(e)}")
                )
