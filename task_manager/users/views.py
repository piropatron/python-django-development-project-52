from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import UserChangeForm, UserForm

from django.utils.translation import gettext_lazy as _
from ..tasks.models import Task


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:15]
        return render(
            request,
            "users/index.html",
            context={
                "users": users,
            },
        )


class CreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(
            request,
            "users/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():  # Если данные корректные, то сохраняем данные формы
            form.save()
            messages.add_message(request, messages.INFO, _('The user has been successfully registered.'))
            return redirect('login')  # Редирект на указанный маршрут
        # Если данные некорректные, то возвращаем человека обратно на страницу с заполненной формой
        return render(request, 'users/create.html', {'form': form})


class UpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if request.user.id is not user_id:
            messages.add_message(request, messages.INFO, _("You do not have permission to make changes."))
            return redirect("users.index")

        user = User.objects.get(id=user_id)
        form = UserChangeForm(instance=user)
        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = User.objects.get(id=user_id)
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("User successfully modified"))

            return redirect("users.index")

        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )


class DeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        return render(
            request, "users/delete.html", {"user_id": user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = get_object_or_404(User, id=user_id)
        if Task.objects.filter(author=user).exists() or Task.objects.filter(executor=user).exists():
            messages.error(request, _("Unable to delete user"))
            return redirect('users.index')


        user.delete()
        messages.add_message(request, messages.INFO, _("User successfully deleted"))

        return redirect("users.index")

