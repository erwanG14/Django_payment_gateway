from .models import SessionMarchand,Token
import uuid
import requests


def send_transaction_to_banque(transaction,url):
        
        transactionData = {
              "banque" : transaction.banque,
              "numero_carte" : transaction.carte.numero_carte,
              "nom_client" : transaction.carte.client.nom,
              "prenom_client" : transaction.carte.client.prenom,
              "montant_transaction" : transaction.prix_transaction
        }

        response = requests.post(url,json=transactionData)
        return response


def create_session(nom,prix):

    token = Token.objects.create(code = uuid.uuid4())
    nom_objet = nom
    prix_transaction = prix
    return SessionMarchand.objects.create(token=token, nom_objet=nom_objet, prix_transaction=prix_transaction)