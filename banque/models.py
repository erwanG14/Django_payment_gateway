from django.db import models

# Create your models here.

class Client_banque(models.Model):

    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    info_bancaire = models.CharField(max_length=20)

    class Meta:

        constraints  = [
            models.UniqueConstraint(
                fields=["nom", "prenom", "info_bancaire"],
                name= "unique_client_banque_constraint",
            )
        ]

    def __str__(self):

        return str(self.nom) +  str(self.prenom)
    
class compte_bancaire(models.Model):

    Client_banque = models.ForeignKey(Client_banque,on_delete=models.CASCADE)
    solde = models.FloatField(default=0)
    def verif_compte(self,data):

        if self.solde - data["montant"] > 0 :

            if self.Client_banque.nom == data["nom"]:

                if self.Client_banque.prenom == data["prenom"]:

                    if self.Client_banque.info_bancaire == data["info_bancaire"]:
                        
                        return {"refus" : False}
                    
                
        return {"refus" : True}