import secrets

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        url = self.request.build_absolute_uri(reverse('users:email-confirm', kwargs={'token': user.token}))

        # Отправка приветственного письма
        subject = 'Добро пожаловать в наш сервис!'
        message = (
            f'Приветствуем, {self.object.email}!\n'
            f'Спасибо за регистрацию на нашем сайте.\n'
            f'Перейдите по ссылке чтобы подвердить почту {url}\n'
            f'С уважением,\n'
            f'Команда сервиса'
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            'Вы успешно зарегистрировались! Проверьте вашу почту для получения приветственного письма.'
        )
        return response


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect("users:login")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')


def user_logout(request):
    logout(request)
    return redirect('catalog:home')
