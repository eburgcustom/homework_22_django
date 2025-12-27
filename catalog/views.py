from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'title': 'Главная - Каталог товаров'
    }
    return render(request, 'home.html', context)


def contacts(request):
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику сохранения в базу данных
        # или отправки email

        # Выводим сообщение об успешной отправке
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('catalog:contacts')

    return render(request, 'contacts.html')


def product_detail(request, pk):
    """
    Отображает детальную информацию о товаре
    """
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'title': f'Товар: {product.name}'
    }
    return render(request, 'product_detail.html', context)
