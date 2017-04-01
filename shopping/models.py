from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
    products = models.ManyToManyField(Product, related_name="shopping_carts", blank=True, through="Purchasable")

    def purchase(self):
        """
            Purchase the products currently in the shopping cart.
        """
        pass

    def add_product(self, product_id, quantity=1):
        """
            Add a product to this cart.
            :returns: the current list of products in the cart.
        """
        try:
            product = Product.objects.get(pk=product_id)
            remaining_units = product.available_inventory - quantity

            if remaining_units > 0:
                purchasable = Purchasable(product=product, shopping_cart=self, quantity=quantity)
                purchasable.save()
            else:
                raise Exception("Too many units of {0} selected!".format(product.title))

            return self.products.all()
        except ObjectDoesNotExist:
            raise Exception("Cannot add a non-existent product!")


    def remove_product(self, product_id, quantity=1):
        """
            Remove a product from this cart.
        """
        try:
            product = Product.objects.get(pk=product_id)
            try:
                purchasable = Purchasable.objects.get(product=product, shopping_cart=self)
                purchasable.delete()
            except ObjectDoesNotExist:
                print "Purchasable object not found, ignoring."
            return self.products.all()
        except ObjectDoesNotExist:
            raise Exception("Cannot remove a non-existent product in the cart!")


class Purchasable(models.Model):
    """
        The through table for products that are in a shopping cart.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class PurchaseHistory(models.Model):
    """
        The purchase history for a specific user.
    """
    owner = models.ForeignKey(User, related_name="purchase_history")
    created = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="purchase_histories")
