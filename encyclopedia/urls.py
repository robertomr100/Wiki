from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryName>",views.entry, name="entry"),
    path("add",views.add,name="add"),
    path("random",views.randomPage,name="random"),
    path("wiki/<str:entryName>/edit",views.edit, name="edit")
]
