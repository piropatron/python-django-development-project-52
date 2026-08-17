from django.urls import path

from .views import (
    CreateView,
    DeleteView,
    IndexView,
    UpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="tags.index"),
    path("create/", CreateView.as_view(), name="tags.create"),
    path("<int:pk>/update/", UpdateView.as_view(), name="tags.update"),
    path("<int:pk>/delete/", DeleteView.as_view(), name="tags.delete"),
]