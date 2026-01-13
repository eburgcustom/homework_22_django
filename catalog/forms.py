from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

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
