from django.urls import path

from . import views

urlpatterns = [
    path("", views.liste_objet, name="liste_objet"),
]