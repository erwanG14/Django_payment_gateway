from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from unittest.mock import patch, Mock

from .models import Item

# Create your tests here.


# -----------------------------------------------Test Model----------------------------------------------------------------------------------
class ItemTestCase(TestCase):
    def test_negative_prices_object(self):
        # an object can't have a negative price
        item = Item(price=-10, nom="mauvais produit")
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_negative_prices_object_db(self):
        # an object can't have a negative price
        with self.assertRaises(IntegrityError):
            Item.objects.create(price=-10, nom="bad")


# --------------------------------------------------Test View--------------------------------------------------------------------------------


class catalogueTestCase(TestCase):
    @patch("site_marchand.views.get_object_or_404")
    def test_paying_negative_price_item(self, mock_get_object):

        # an object with a negative price can't be bought and need to be sent to an error when "payer" is clicked

        fake_item = Mock()
        fake_item.id = 1
        fake_item.name = "aspirateur"
        fake_item.price = -100
        mock_get_object.return_value = fake_item

        response = self.client.get(
            reverse("initier"), {"id": fake_item.id}, follow=True
        )

        self.assertContains(response, "prix invalide", status_code=400)
