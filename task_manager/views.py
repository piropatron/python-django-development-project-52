from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
            context={},
        )


class CustomLoginView(LoginView):
    # Укажите URL для перенаправления после входа
    success_url = reverse_lazy('home')  # замените на свой именованный URL

    def form_valid(self, form):
        # Вызываем родительский метод, который выполняет аутентификацию и редирект
        response = super().form_valid(form)
        # Добавляем сообщение об успехе
        messages.success(self.request, "Вы залогинены")
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # куда перенаправить после выхода

    def post(self, request, *args, **kwargs):
        # Сначала вызываем родительский метод, он выполнит выход и вернёт редирект
        response = super().post(request, *args, **kwargs)
        # Добавляем сообщение об успешном выходе
        messages.success(request, "Вы разлогинены")
        return response