from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


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
