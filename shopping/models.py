from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
        A product that can be purchased.
    """
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    available_inventory = models.IntegerField(null=True, blank=True)


class ShoppingCart(models.Model):
    """
        A shopping cart for a specific user.
    """
    owner = models.OneToOneField(User, related_name="shopping_cart")
    products = models.ManyToManyField(Product, related_name="shopping_carts", blank=True)

    def purchase(self):
        """
            Purchase the products currently in the shopping cart.
        """
        pass

    def addProduct(self, product_id):
        """
            Add a product to this cart.
        """
        pass

    def removeProduct(self, product_id):
        """
            Remove a product from this cart.
        """
        pass


class PurchaseHistory(models.Model):
    """
        The purchase history for a specific user.
    """
    owner = models.ForeignKey(User, related_name="purchase_history")
    created = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="purchase_histories")
