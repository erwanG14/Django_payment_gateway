from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

import uuid

# Create your models here.



class Client(models.Model):

    bank = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)

    class Meta: 
        constraints = [
            models.UniqueConstraint(
               fields=["bank","name","surname"],
               name = "unique_client_constraint"
            )
        ]
    
    def __str__(self):
        return  str(self.id)+"-"+ str(self.name) +"-" +str(self.surname)   
    
    
    
    
class Card(models.Model):

    card_data = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(12)]
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta: 
        constraints = [
            models.UniqueConstraint(
               fields=["card_data"],
               name = "unique_card_constraint"
            )
        ]

    def __str__(self):
        return  str(self.card_data)


    
class TransactionStatus(models.TextChoices):

    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    AUTHORIZED = "authorized", "Authorized"
    CAPTURED = "captured", "Captured"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    REFUSED = "refused", "Refused"


class Transaction(models.Model):

    idempotency_key = models.UUIDField(
        default = uuid.uuid4,
        unique = True,
        editable = True,
    )

    bank = models.CharField(max_length=40)
    price_transaction = models.IntegerField()

    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    transaction_status = models.CharField(
        max_length = 20,
        choices = TransactionStatus.choices,
        default = TransactionStatus.PENDING,
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return  str(str(self.id) +"-"+str(self.transaction_status))
    
class SessionMarchand(models.Model):

    idempotency_key = models.CharField(max_length=255,unique=True)
    code_url =  models.UUIDField(
    default=uuid.uuid4,
    unique=True,
    editable=True
    )

    item_name = models.CharField(max_length=50)
    price_transaction = models.IntegerField()

    status = models.CharField(max_length=30, default="pending")

    created_at = models.DateTimeField(default=timezone.now)
    
    


