from django.urls import path

from . import views

urlpatterns = [
    path("catalogue",views.CatalogueView.as_view() , name="catalogue"),
    path("echec_paiement", views.echec_paiement, name="echec_paiement"),
    path(
        "reussite_paiement", views.reussite_paiement, name="reussite_paiement"
    ),
]
