from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import LabelChangeForm, LabelCreateForm

# Create your views here.
from .models import Label


# Create your views here.
class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()[:15]
        return render(
            request,
            "labels/index.html",
            context={
                "labels": labels,
            },
        )


class CreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelCreateForm()
        return render(
            request,
            "labels/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = LabelCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Label successfully created'))
            return redirect('labels.index')

        return render(request, 'labels/create.html', {'form': form})


class DeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get("pk")

        return render(
            request, "labels/delete.html", {"label_id": label_id}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("pk")
        label = get_object_or_404(Label, id=label_id)
        if label.tasks.exists():
            messages.error(request, _("Unable to delete label"))
            return redirect('labels.index')

        label.delete()
        messages.add_message(request, messages.INFO, _("Label successfully deleted"))

        return redirect("labels.index")


class UpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get("pk")
        user = Label.objects.get(id=label_id)
        form = LabelChangeForm(instance=user)
        return render(
            request, "labels/update.html", {"form": form, "label_id": label_id}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("pk")
        user = Label.objects.get(id=label_id)
        form = LabelChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Label successfully modified"))

            return redirect("labels.index")

        return render(
            request, "labels/update.html", {"form": form, "label_id": label_id}
        )