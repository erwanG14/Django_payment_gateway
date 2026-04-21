from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Objet
# Create your tests here.

#-----------------------------------------------Test Model----------------------------------------------------------------------------------
class ObjetTestCase(TestCase):
    def test_negative_prices_object(self):
        # an object can't have a negative price
        objet = Objet(prix = -10, nom="mauvais produit")
        with self.assertRaises(ValidationError):
            objet.full_clean()

    def test_negative_prices_object_db(self):
        # an object can't have a negative price
        with self.assertRaises(IntegrityError):
            Objet.objects.create(prix=-10, nom="bad")




#--------------------------------------------------Test View--------------------------------------------------------------------------------

class catalogueTestCase(TestCase):
    def test_paying_negative_price_object(self):
        # an object with a negative price can't be bought and need to be sent to an error when "payer" is clicked
        objet = Objet(prix = -10, nom="mauvais produit")
        
    
