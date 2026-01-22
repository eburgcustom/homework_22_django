from django.shortcuts import  redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка приветственного письма
        subject = 'Добро пожаловать в наш сервис!'
        message = (
            f'Приветствуем, {self.object.email}!\n\n'
            'Спасибо за регистрацию на нашем сайте.\n'
            'С уважением,\n'
            'Команда сервиса'
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            'Вы успешно зарегистрировались! Проверьте вашу почту для получения приветственного письма.'
        )
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')


def user_logout(request):
    logout(request)
    return redirect('catalog:home')
