from django.urls import path

from . import views

urlpatterns = [
    path("paiement/", views.paiement, name="paiement"),
]