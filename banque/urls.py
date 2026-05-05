from django.urls import path

from . import views

urlpatterns = [
    path(
        "reception_transaction/",
        views.reception_transaction,
        name="reception_transaction",
    ),
]
