from django.contrib import admin
from .models import Client, Transaction, Card, SessionMarchand
# Register your models here.

admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(Card)
admin.site.register(SessionMarchand)