import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    labels = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label=_('Label'),
    )
    only_my_task = django_filters.BooleanFilter(
        method='filter_only_my_task',
        widget=forms.CheckboxInput(),
        label=_('Only my task'),
    )

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'executor': ['exact'],
            'labels': ['exact'],
        }

    def filter_only_my_task(self, queryset, name, value):
        # value — это True или False в зависимости от состояния чекбокса
        if value:
            # Получаем текущего пользователя из запроса
            user = self.request.user

            if user and user.is_authenticated:
                return queryset.filter(author=user)
        return queryset