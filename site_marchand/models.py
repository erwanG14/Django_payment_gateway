from django.db import models
from django.utils import timezone

import uuid

# Create your models here.

class Item(models.Model):

    price = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class SessionStatus(models.TextChoices):

    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"

class Session(models.Model):

    idempotency_key = models.UUIDField(
        default = uuid.uuid4,
        unique = True,
        editable = False
    )

    item = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)

    session_status = models.CharField(
        max_length = 20,  
        choices = SessionStatus.choices,
        default = SessionStatus.PENDING,
    )
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    



