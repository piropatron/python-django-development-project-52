from django import forms

from task_manager.tags.models import Tag


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            "name",
        ]


class TagChangeForm(TagCreateForm):
    pass
