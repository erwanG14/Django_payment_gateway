from django.db import models
from django.http import JsonResponse
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Create your models here.


class Token(models.Model):
    
    code = models.CharField(max_length=100)
    def __str__(self):
        return  str(self.code)

class Client(models.Model):

    banque = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=40)
    
    def __str__(self):
        return  str(self.id)+"-"+ str(self.nom) +"-" +str(self.prenom)   
    
    class Meta: 
        constraints = [
            models.UniqueConstraint(
               fields=["banque","nom","prenom"],
               name = "unique_client_constraint"
            )
        ]
    
    
class Carte(models.Model):

    numero_carte = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(12)]
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta: 
        constraints = [
            models.UniqueConstraint(
               fields=["numero_carte"],
               name = "unique_card_constraint"
            )
        ]

    def __str__(self):
        return  str(self.numero_carte)


    
class TransactionStatus(models.TextChoices):

    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    AUTHORIZED = "authorized", "Authorized"
    CAPTURED = "captured", "Captured"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    REFUSED = "refused", "Refused"


class Transaction(models.Model):

    banque = models.CharField(max_length=40)
    carte = models.ForeignKey(Carte, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    prix_transaction = models.IntegerField()

    transaction_status = models.CharField(
        max_length = 20,
        choices = TransactionStatus.choices,
        default = TransactionStatus.PENDING,
    )

    def __str__(self):
        return  str(str(self.id) +"-"+str(self.transaction_status))
    
    #token lié au client donc contrainte sur transaction pas utile
    """class Meta:
        constraints  = [
            models.UniqueConstraint(
                fields=["token", "prix_transaction", "info_carte", "refus"],
                name= "unique_payment_constraint",
            )
        ]""" 
    
class SessionMarchand(models.Model):

    nom_objet = models.CharField(max_length=50)
    prix_transaction = models.IntegerField()
    idempotency_key = models.CharField(max_length=255,unique=True)
    status = models.CharField(max_length=30, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    


