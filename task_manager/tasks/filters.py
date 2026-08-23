import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    status = django_filters.ModelChoiceFilter(
        field_name='status',
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={
            'class': 'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base ' +
                     'text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 ' +
                     'focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}),
    )

    labels = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={
            'class': 'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3' +
                     ' text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300' +
                     ' focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}),
    )

    executor = django_filters.ModelChoiceFilter(
        field_name='executor',
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(
            attrs={
                'class': 'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 ' +
                         'pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 ' +
                         'focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}
        ),
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
        if value:
            user = self.request.user

            if user and user.is_authenticated:
                return queryset.filter(author=user)
        return queryset