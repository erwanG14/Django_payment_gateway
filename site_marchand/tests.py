from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from django.urls import reverse
from unittest.mock import patch, Mock

from .models import Objet
# Create your tests here.

#-----------------------------------------------Test Model----------------------------------------------------------------------------------
class ObjetTestCase(TestCase):
    
    def test_negative_prices_object(self):

        # an object can't have a negative price
        objet = Objet(prix=-10, nom="mauvais produit")
        with self.assertRaises(ValidationError):
            objet.full_clean()

    def test_negative_prices_object_db(self):
        # an object can't have a negative price
        with self.assertRaises(IntegrityError):
            Objet.objects.create(prix=-10, nom="bad")




#--------------------------------------------------Test View--------------------------------------------------------------------------------

class catalogueTestCase(TestCase):
    @patch("site_marchand.views.get_object_or_404")

    def test_paying_negative_price_object(self, mock_get_object):

        # an object with a negative price can't be bought and need to be sent to an error when "payer" is clicked
        
        faux_objet = Mock()
        faux_objet.id = 1
        faux_objet.nom = 'aspirateur'
        faux_objet.prix = -100
        mock_get_object.return_value = faux_objet

        response = self.client.get(
            reverse('initier'),
            {'id': faux_objet.id},
            follow=True
            )
        
        self.assertContains(response, "prix invalide", status_code=400)

    
