from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View, generic

from .filters import TaskFilter
from .forms import TaskCreateForm
from .models import Task


# Create your views here.
class CreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render(
            request,
            "tasks/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.add_message(request, messages.INFO, _('Task successfully created'))
            return redirect('tasks.index')

        return render(request, 'tasks/create.html', {'form': form})


class DeleteView(View):
    pass


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        filter = TaskFilter(request.GET, request=request, queryset=Task.objects.all())
        tasks = filter.qs
        paginator = Paginator(tasks, 2)  # 10 задач на страницу
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "tasks/index.html",
            context={
                "tasks_list": page_obj,
                'filter': filter
            },
        )


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        form = TaskCreateForm(instance=task)
        return render(
            request,
            "tasks/update.html",
            context={
                "form": form,
                'task_id': task_id,
            },
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Task successfully updated'))
            return redirect('tasks.index')

        return render(request, 'tasks/update.html', {'form': form, 'task_id': task_id})


class DetailView(generic.DetailView):
    model = Task
    template_name = "tasks/detail.html"
