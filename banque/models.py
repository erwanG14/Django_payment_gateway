from django.db import models

# Create your models here.

class ClientBanque(models.Model):

    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    numero_carte = models.CharField(max_length=20)

    class Meta:

        constraints  = [
            models.UniqueConstraint(
                fields=["nom", "prenom", "numero_carte"],
                name= "unique_client_banque_constraint",
            )
        ]

    def __str__(self):

        return str(self.nom) +  str(self.prenom)
    
class CompteBancaire(models.Model):
    
    client_banque = models.ForeignKey(ClientBanque,on_delete=models.CASCADE)
    solde = models.FloatField(default=0)

    class Meta:

        constraints  = [
            models.UniqueConstraint(
                fields=["client_banque",],
                name= "unique_CompteBancaire_constraint",
            )
        ]