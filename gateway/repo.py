from .models import Card, Client, Transaction, SessionMarchand

def create_client(bank,name,surname):
    return Client.objects.get_or_create( #renvoi un tuple
        bank=bank,
        name=name,
        surname=surname
    )[0]
def create_card(card_data,client):
    return Card.objects.get_or_create( #renvoi un tuple
        card_data=card_data,
        client=client
    )[0]
def create_transaction(bank,price_transaction,card):
    return Transaction.objects.create(
        bank=bank,
        price_transaction=price_transaction,
        card=card
    )
def get_session_marchande(url_code):
    return SessionMarchand.objects.get(url_code=url_code)