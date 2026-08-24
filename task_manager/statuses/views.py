from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from ..tasks.models import Task
from .forms import StatusChangeForm, StatusCreateForm
from .models import Status


# Create your views here.
class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            "statuses/index.html",
            context={
                "statuses": statuses,
            },
        )


class CreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StatusCreateForm()
        return render(
            request,
            "statuses/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Status successfully created'))
            return redirect('statuses.index')

        return render(request, 'statuses/create.html', {'form': form})


class DeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")

        return render(
            request, "statuses/delete.html", {"status_id": status_id}
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = get_object_or_404(Status, id=status_id)
        if Task.objects.filter(status=status).exists():
            messages.error(request, _("Unable to delete status"))
            return redirect('statuses.index')

        status.delete()
        messages.add_message(request, messages.INFO, _("Status successfully deleted"))

        return redirect("statuses.index")


class UpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(id=status_id)
        form = StatusChangeForm(instance=status)
        return render(
            request, "statuses/update.html", {"form": form, "status_id": status_id}
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        user = Status.objects.get(id=status_id)
        form = StatusChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Status successfully modified"))

            return redirect("statuses.index")

        return render(
            request, "statuses/update.html", {"form": form, "status_id": status_id}
        )