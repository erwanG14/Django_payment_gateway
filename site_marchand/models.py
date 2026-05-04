from django.db import models
from django.utils import timezone

import uuid

# Create your models here.

class Objet(models.Model):
    prix = models.PositiveIntegerField(default=0)
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.nom
    
class SessionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"

class Session(models.Model):
    objet = models.CharField(max_length=50)
    ammount = models.IntegerField(default=0)
    session_status = models.CharField(
        max_length = 20,  
        choices = SessionStatus.choices,
        default = SessionStatus.PENDING,
    )

    idempotency_key = models.UUIDField(
        default = uuid.uuid4,
        unique = True,
        editable = False
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    



