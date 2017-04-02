from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal


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
            Purchase the products currently in the shopping cart and creates a history record for it.
            :returns: PurchaseHistory instance
        """
        purchasables = Purchasable.objects.filter(shopping_cart=self)
        purchase_history = PurchaseHistory(owner=self.owner)
        purchase_history.save()
        total_cost = Decimal(0)

        # validate the purchase (ensuring there's enough units to make the purchase)
        for purchasable in purchasables:
            product = purchasable.product
            if product.available_inventory - purchasable.quantity < 0:
                purchase_history.delete()
                raise Exception("Unit quantity exceeded for purchase of {0}".format(product.title))

        # go through and purchase the items and store it in the history.
        for purchasable in purchasables:
            product = purchasable.product
            product.available_inventory = product.available_inventory - purchasable.quantity
            product.save()

            final_cost = purchasable.quantity * product.price
            purchased = Purchased(purchase_history=purchase_history,
                                  product=product,
                                  quantity=purchasable.quantity,
                                  cost=final_cost)
            purchased.save()
            total_cost += final_cost

        purchase_history.cost = total_cost
        purchase_history.save()

        return purchase_history

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


class PurchaseHistory(models.Model):
    """
        The purchase history for a specific user.
    """
    # TODO: perhaps the related_name should be changed to something else.
    owner = models.ForeignKey(User, related_name="purchase_history")
    created = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="purchase_histories", through="Purchased")
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

# --------------
# Through Tables
# --------------

class Purchasable(models.Model):
    """
        The through table for products that are in a shopping cart.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Purchased(models.Model):
    """
        The through table for products that were purchased.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_history = models.ForeignKey(PurchaseHistory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
