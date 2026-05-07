from.models import ClientBank, BankAccount

def get_client_compte(name,surname,card_data):
    try:
        client = ClientBank.objects.get(
            name=name,
            surname=surname,
            card_data=card_data,
        )

        compte = BankAccount.objects.get(
            client_bank=client,
        )
        return compte
    except ClientBank.DoesNotExist:
        return False
    except BankAccount.DoesNotExist:
        return False