from django.urls import path

from . import views

urlpatterns = [
    path("paiement/<uuid:url_code>/", views.PaiementView.as_view(), name="paiement"),
    path(
        "recevoir_transaction_marchand/",
        views.recevoir_transaction_marchand,
        name="recevoir_transaction_marchand",
    ),
]
