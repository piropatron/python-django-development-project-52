from django import forms

from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'author',
            'executor',
            'labels',
        ]
        exclude = ['author']
        widgets = {
            'status': forms.Select(
                attrs={'class': 'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white ' +
                                                   'py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 ' +
                                                   'outline-gray-300 focus:outline-2 focus:-outline-offset-2 ' +
                                                   'focus:outline-indigo-600 sm:text-sm/6'}),
            'executor': forms.Select(
                attrs={'class': 'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white ' +
                                                     'py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1' +
                                                     ' -outline-offset-1 outline-gray-300 focus:outline-2' +
                                                     ' focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
                                            }),
            'labels': forms.SelectMultiple(
                attrs={'class': 'col-start-1 row-start-1 w-full appearance-none ' +
                                                           'rounded-md bg-white py-1.5 pr-8 pl-3 text-base ' +
                                                           'text-gray-900 outline-1 -outline-offset-1 outline-gray-300' +
                                                           ' focus:outline-2 focus:-outline-offset-2 '
                                                           'focus:outline-indigo-600 sm:text-sm/6'}
            ),
        }