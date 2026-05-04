from .models import ClientBanque,CompteBancaire
def get_client_compte(data_client):
    try:
          client = ClientBanque.objects.get(
               nom = data_client["nom"],
               prenom = data_client["prenom"],
               numero_carte = data_client["numero_carte"],
          )

          compte = CompteBancaire.objects.get(
             client_banque = client,
          )
          return compte
    except ClientBanque.DoesNotExist:
         return False
    except CompteBancaire.DoesNotExist:
         return False
    


def verif_compte(data_client,data_transaction):
    compte = get_client_compte(data_client)
    if not compte:
        return {"refus" : True , "reason" : "no acccount"}
    else:
        if compte.solde - data_transaction["montant"] > 0 :

            if compte.ClientBanque.nom == data_transaction["nom"]:

                if compte.ClientBanque.prenom == data_transaction["prenom"]:

                    if compte.ClientBanque.numero_carte == data_transaction["numero_carte"]:
                        
                        return {"refus" : False}
                    
                
        return {"refus" : True}