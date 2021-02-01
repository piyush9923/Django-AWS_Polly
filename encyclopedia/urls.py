from django.urls import path

from . import views

app_name = "wikipedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.info, name='title'),
    path("search", views.search, name='search'),
    path("create", views.create, name='create'),
    path("random", views.random_page, name='random'),
    path("wiki/<title>/edit", views.edit, name='edit')
]
