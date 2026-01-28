from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'publication_status', 'is_published')
    list_filter = ('category', 'publication_status', 'is_published')
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')
    list_editable = ('publication_status', 'is_published')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Публикация', {
            'fields': ('is_published', 'publication_status'),
            'classes': ('collapse',)
        }),
    )
