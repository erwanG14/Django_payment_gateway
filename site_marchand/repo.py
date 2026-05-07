from django.shortcuts import get_object_or_404

from .models import Item, Session

import uuid

def get_item_404(id_item):
    return get_object_or_404(
        Item,
        id=id_item
    )
def create_session(item):
    session = Session.objects.create(
        item=item.name,
        amount=item.price,
        idempotency_key=uuid.uuid4(),
        session_status="pending",
    )

    return session