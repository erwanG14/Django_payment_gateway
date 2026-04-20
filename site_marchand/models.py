from django.db import models
import uuid

# Create your models here.

#Transaction : token, montant
#Objet : prix, noms
# on ne peut acheter qu'un seul objet sur ce site

class Objet(models.Model):
    prix = models.IntegerField(default=0)
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.nom

class Session(models.Model):
    objet = models.CharField(max_length=50)
    ammount = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)
    
def Create_Session(produit):
    objet = produit
    ammount = produit.prix
    Session.objects.create(objet=objet, ammount=ammount)
    


