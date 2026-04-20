from django.urls import path

from . import views

urlpatterns = [
    path("catalogue", views.catalogue, name="catalogue"),
    path("initier/", views.initier, name="initier"),
]