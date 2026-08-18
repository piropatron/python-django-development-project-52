from django.urls import path

from .views import (
    CreateView,
    DeleteView,
    IndexView,
    UpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="labels.index"),
    path("create/", CreateView.as_view(), name="labels.create"),
    path("<int:pk>/update/", UpdateView.as_view(), name="labels.update"),
    path("<int:pk>/delete/", DeleteView.as_view(), name="labels.delete"),
]