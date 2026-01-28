from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Товар успешно удален!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление товара: {self.object.name}'
        return context
