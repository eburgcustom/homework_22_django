from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product


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


class ProductDetailView(DetailView):
    """
    Класс для отображения детальной информации о товаре
    """
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Товар: {self.object.name}'
        return context
