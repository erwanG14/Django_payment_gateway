from django.contrib import admin
from .models import Client, Transaction, Token,Carte,SessionMarchand
# Register your models here.

admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(Token)
admin.site.register(Carte)
admin.site.register(SessionMarchand)