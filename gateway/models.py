from django.db import models
import uuid

# Create your models here.
# token : code
# client : banque info carte (crypté) clé etrangere token
# transaction : clé etrangere token info carte banque refus default true

class Token(models.Model):
    code = models.CharField(max_length=100)
    def __str__(self):
        return  str(self.id)

class Client(models.Model):
    banque = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=40)
    info_carte = models.CharField(max_length=20)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    def __str__(self):
        return  str(self.id)
    
class Transaction(models.Model):
    banque = models.CharField(max_length=40)
    info_carte = models.CharField(max_length=20)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    refus = models.BooleanField(default=True)
    def __str__(self):
        return  str(str(self.id) +"-"+str(self.refus))
    
class Session_marchand(models.Model):
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    nom_objet = models.CharField(max_length=50)
    prix_transaction = models.IntegerField()
    
def create_session(nom,prix):
    token = Token.objects.create(code = uuid.uuid4())
    nom_objet = nom
    prix_transaction = prix
    return Session_marchand.objects.create(token=token, nom_objet=nom_objet, prix_transaction=prix_transaction)


