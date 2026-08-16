from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusCreateForm, StatusChangeForm


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()[:15]
        return render(
            request,
            "statuses/index.html",
            context={
                "statuses": statuses,
            },
        )


class CreateView(View):
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



class DeleteView(View):
    pass


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        user = Status.objects.get(id=status_id)
        form = StatusChangeForm(instance=user)
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