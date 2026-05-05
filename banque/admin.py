from django.contrib import admin
from .models import ClientBank,BankAccount

# Register your models here.
admin.site.register(ClientBank)
admin.site.register(BankAccount)