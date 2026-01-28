from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """
    Класс для отображения списка товаров на главной странице
    """
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            is_published=True,
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Класс для отображения детальной информации о товаре
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

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
        return super().form_valid(form)

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
        return super().form_valid(form)

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
        response = super().delete(request, *args, **kwargs)
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Отмена публикации: {self.object.name}'
        return context
    
    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.REJECTED
        form.instance.is_published = False
        messages.success(self.request, f'Продукт "{self.object.name}" снят с публикации')
        return super().form_valid(form)


class ProductPublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс для публикации продукта
    """
    model = Product
    template_name = 'catalog/product_publish.html'
    permission_required = 'catalog.can_unpublish_product'
    success_url = reverse_lazy('catalog:moderation_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Публикация: {self.object.name}'
        return context
    
    def form_valid(self, form):
        form.instance.publication_status = Product.PublicationStatus.PUBLISHED
        form.instance.is_published = True
        messages.success(self.request, f'Продукт "{self.object.name}" успешно опубликован')
        return super().form_valid(form)
