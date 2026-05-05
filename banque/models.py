from django.db import models

# Create your models here.


class ClientBank(models.Model):

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    card_data = models.CharField(max_length=20)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["name", "surname", "card_data"],
                name="unique_client_bank_constraint",
            )
        ]

    def __str__(self):

        return str(self.name) + str(self.surname)


class BankAccount(models.Model):

    client_bank = models.ForeignKey(ClientBank, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["client_bank"],
                name="unique_BankAccount_constraint",
            )
        ]
