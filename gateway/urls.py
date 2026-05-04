from django.urls import path

from .views import PaiementView
from . import views

urlpatterns = [
    path("paiement/<int:session_id>/", PaiementView.as_view(), name="paiement"),
    path("recevoir_transaction_marchand/", views.recevoir_transaction_marchand, name="recevoir_transaction_marchand"),
]