from django.urls import path

from . import views

urlpatterns = [
    path("catalogue", views.catalogue, name="catalogue"),
    path("initier/", views.initier, name="initier"),
    path("initier/echec_paiement",views.echec_paiement,name="echec_paiement"),
    path("initier/reussite_paiement",views.reussite_paiement,name="reussite_paiement"),
]