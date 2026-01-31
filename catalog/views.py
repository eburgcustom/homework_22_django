from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category


class ProductListView(ListView):
    """
    Класс для отображения списка товаров на главной странице
    """
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            publication_status=Product.PublicationStatus.PUBLISHED
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная - Каталог товаров'
        return context


class ContactsView(TemplateView):
    """
    Класс для отображения страницы контактов с формой обратной связи
    """
    template_name = 'contacts.html'

    def post(self, request, *args, **kwargs):
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Выводим сообщение об успешной отправке
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('catalog:contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class ProductDetailView(DetailView):
    """
    Класс для отображения детальной информации о товаре
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        cache_key = f'product_{obj.id}'
        cached_obj = cache.get(cache_key)
        if cached_obj is None:
            cache.set(cache_key, obj, 60 * 15)  # Кэш на 15 минут
            return obj
        return cached_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Товар: {self.object.name}'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания нового товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан!')
        response = super().form_valid(form)
        # Очистка кэша при создании нового товара
        cache.delete(f'product_{self.object.id}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для редактирования товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # Проверяем, что пользователь является владельцем или модератором
        if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(request, 'У вас нет прав для редактирования этого товара')
            return redirect('catalog:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен!')
        response = super().form_valid(form)
        # Очистка кэша при обновлении товара
        cache.delete(f'product_{self.object.id}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование товара: {self.object.name}'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления товара
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    context_object_name = 'product'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # Проверяем, что пользователь является владельцем или модератором
        if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(request, 'У вас нет прав для удаления этого товара')
            return redirect('catalog:home')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        product_id = self.get_object().id
        response = super().delete(request, *args, **kwargs)
        # Очистка кэша при удалении товара
        cache.delete(f'product_{product_id}')
        messages.success(self.request, 'Товар успешно удален!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление товара: {self.object.name}'
        return context


class ProductModerationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс для отображения списка товаров на модерации
    """
    model = Product
    template_name = 'catalog/product_moderation_list.html'
    context_object_name = 'products'
    permission_required = 'catalog.can_unpublish_product'

    def get_queryset(self):
        return Product.objects.filter(
            publication_status__in=[Product.PublicationStatus.MODERATION, Product.PublicationStatus.DRAFT]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация продуктов'
        return context


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс для отмены публикации продукта
    """
    model = Product
    template_name = 'catalog/product_unpublish.html'
    permission_required = 'catalog.can_unpublish_product'
    success_url = reverse_lazy('catalog:moderation_list')
    fields = []  # Пустые поля, т.к. форма не нужна

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Отмена публикации: {self.object.name}'
        return context

    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.REJECTED
        response = super().form_valid(form)
        # Очистка кэша при отмене публикации
        cache.delete(f'product_{self.object.id}')
        messages.success(self.request, f'Продукт "{self.object.name}" снят с публикации')
        return response


class ProductPublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс для публикации продукта
    """
    model = Product
    template_name = 'catalog/product_publish.html'
    permission_required = 'catalog.can_unpublish_product'
    success_url = reverse_lazy('catalog:moderation_list')
    fields = []  # Пустые поля, т.к. форма не нужна

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Публикация: {self.object.name}'
        return context

    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.PUBLISHED
        response = super().form_valid(form)
        # Очистка кэша при публикации
        cache.delete(f'product_{self.object.id}')
        messages.success(self.request, f'Продукт "{self.object.name}" успешно опубликован')
        return response


class CategoryProductsView(ListView):
    """
    Класс для отображения продуктов в указанной категории
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        context['title'] = f'Категория: {category.name}'
        return context
