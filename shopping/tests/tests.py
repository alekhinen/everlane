from django.test import TestCase
from factories import UserFactory, ProductFactory, ShoppingCartFactory, PurchaseHistoryFactory
from shopping.models import Purchased

# Create your tests here.

class ShoppingCartTest(TestCase):
    def setUp(self):
        # generate some products
        self.shirt = ProductFactory(title="black shirt", price=15.00, available_inventory=200)
        self.button_down = ProductFactory(title="velvet button down", price=150.00, available_inventory=2)
        # generate a shopping cart
        self.shopping_cart = ShoppingCartFactory()

    def test_add_product(self):

        # a shopping cart should start off empty
        self.assertEqual(len(self.shopping_cart.products.all()), 0)

        # adding a product should store it in the list of products.
        products = self.shopping_cart.add_product(self.shirt.pk)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, self.shirt.title)

        products = self.shopping_cart.add_product(self.button_down.pk)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[1].title, self.button_down.title)

        # adding a product that does not exist should throw a custom exception.
        with self.assertRaisesRegexp(Exception, "non-existent product"):
            self.shopping_cart.add_product(-20)

    def test_remove_products(self):
        self.shopping_cart.add_product(self.shirt.pk)
        self.shopping_cart.add_product(self.button_down.pk)

        # removing a product should remove it from the cart's list of products.
        products = self.shopping_cart.remove_product(self.shirt.pk)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, self.button_down.title)

        # removing a product that isn't in the list should not affect the list.
        products = self.shopping_cart.remove_product(self.shirt.pk)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, self.button_down.title)

        # remove a product that does not exist should throw a custom exception.
        with self.assertRaisesRegexp(Exception, "non-existent product"):
            self.shopping_cart.remove_product(-20)

    def test_purchase(self):
        self.shopping_cart.add_product(self.shirt.pk, 5)
        self.shopping_cart.add_product(self.button_down.pk)

        # you should be able to make a purchase and have that store in your history.
        purchase_history = self.shopping_cart.purchase()
        self.assertEqual(purchase_history.cost, 225.00)
        purchases = Purchased.objects.filter(purchase_history=purchase_history).order_by("quantity")
        self.assertEqual(len(purchases), 2)
        self.assertEqual(purchases[0].cost, 150.00)
        self.assertEqual(purchases[1].cost, 75.00)

        # the available inventory should drop because of the purchase
        products = purchase_history.products.all()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].available_inventory, 195)
        self.assertEqual(products[1].available_inventory, 1)

        # you should not be able to make a purchase that exceeds the available inventory.
