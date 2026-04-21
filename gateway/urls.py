from django.urls import path

from . import views

urlpatterns = [
    path("paiement/", views.paiement, name="paiement"),
    path("recevoir_transaction_marchand/", views.recevoir_transaction_marchand, name="recevoir_transaction_marchand"),
]