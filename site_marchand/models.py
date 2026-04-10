from django.db import models

# Create your models here.

#Transaction : token, montant
#Objet : prix, noms
# on ne peut acheter qu'un seul objet sur ce site

class Objet(models.Model):
    prix = models.IntegerField(default=0)
    nom = models.CharField(max_length=50)

class Transaction(models.Model):
    token = models.CharField(max_length=100)
    objet = models.ForeignKey(Objet, on_delete=models.PROTECT)
    ammount = models.IntegerField(default = 0)
    
    
    
    


