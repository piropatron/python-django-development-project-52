from django.urls import path

from .views import (
    CreateView,
    DeleteView,
    DetailView,
    IndexView,
    UpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="tasks.index"),
    path("create/", CreateView.as_view(), name="tasks.create"),
    path("<int:pk>/update/", UpdateView.as_view(), name="tasks.update"),
    path("<int:pk>/delete/", DeleteView.as_view(), name="tasks.delete"),
    path("<int:pk>/", DetailView.as_view(), name="tasks.detail"),
]