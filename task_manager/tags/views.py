from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Tag
from .forms import TagCreateForm, TagChangeForm


# Create your views here.
class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()[:15]
        return render(
            request,
            "tags/index.html",
            context={
                "tags": tags,
            },
        )


class CreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TagCreateForm()
        return render(
            request,
            "tags/create.html",
            context={
                "form": form,
            },
        )
    def post(self, request, *args, **kwargs):
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Tag successfully created'))
            return redirect('tags.index')

        return render(request, 'tags/create.html', {'form': form})



class DeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_id = kwargs.get("pk")

        return render(
            request, "tags/delete.html", {"tag_id": tag_id}
        )

    def post(self, request, *args, **kwargs):
        tag_id = kwargs.get("pk")
        user = get_object_or_404(Tag, id=tag_id)
        user.delete()
        messages.add_message(request, messages.INFO, _("Tag successfully deleted"))

        return redirect("tags.index")


class UpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_id = kwargs.get("pk")
        user = Tag.objects.get(id=tag_id)
        form = TagChangeForm(instance=user)
        return render(
            request, "tags/update.html", {"form": form, "tag_id": tag_id}
        )

    def post(self, request, *args, **kwargs):
        tag_id = kwargs.get("pk")
        user = Tag.objects.get(id=tag_id)
        form = TagChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Tag successfully modified"))

            return redirect("tags.index")

        return render(
            request, "tags/update.html", {"form": form, "tag_id": tag_id}
        )