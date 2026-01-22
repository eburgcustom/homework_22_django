import os
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для всех полей
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            # Добавляем placeholder'ы
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
            # Для чекбокса добавляем отдельный класс
            elif field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'
            # Добавляем обязательные поля
            if field.required:
                field.widget.attrs['required'] = 'required'

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word.lower() in name.lower():
                raise ValidationError(f'Название содержит запрещённое слово: {word}')

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if not description:  # Если описание необязательное
            return description

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word.lower() in description.lower():
                raise ValidationError(f'Описание содержит запрещённое слово: {word}')

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Если изображение не загружено, пропускаем валидацию
        if not image:
            return image

        # Проверка размера файла (5MB = 5 * 1024 * 1024 bytes)
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError(f'Размер изображения не должен превышать 5 МБ. Ваш файл: {filesizeformat(image.size)}')

        # Проверка формата файла
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError('Поддерживаются только изображения в формате JPG или PNG')

        return image
