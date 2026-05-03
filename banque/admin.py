from django.contrib import admin
from .models import Client_banque,compte_bancaire

# Register your models here.
admin.site.register(Client_banque)
admin.site.register(compte_bancaire)